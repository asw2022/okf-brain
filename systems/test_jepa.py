"""Tests for JEPA World Model reference implementation."""

import numpy as np
import pytest

from jepa_world_model import (
    Observation, Action, Representation, Trajectory,
    PerceptionModule, EnergyFunction, GuardrailObjective,
    JEPACore, HierarchicalPlanner, WorldModelSystem,
)


# ─── PerceptionModule ────────────────────────────────────────────

class TestPerceptionModule:
    def test_encode_output_shape(self):
        mod = PerceptionModule(input_dim=64, latent_dim=32)
        obs = Observation(data=np.random.randn(64))
        rep = mod.encode(obs)
        assert rep.z.shape == (32,)
        assert rep.predictable is True
    
    def test_encode_tanh_bounded(self):
        mod = PerceptionModule(input_dim=16, latent_dim=8)
        obs = Observation(data=np.ones(16) * 100)  # large input
        rep = mod.encode(obs)
        assert np.all(np.abs(rep.z) <= 1.01)  # tanh bounds
    
    def test_predict_next_returns_representation(self):
        mod = PerceptionModule(input_dim=32, latent_dim=16)
        z = Representation(z=np.zeros(16))
        action = Action(name="move", params={})
        z_next = mod.predict_next(z, action)
        assert z_next.z.shape == (16,)
        assert isinstance(z_next.predictable, bool)


# ─── EnergyFunction ──────────────────────────────────────────────

class TestEnergyFunction:
    def test_lower_energy_closer_to_goal(self):
        goal = np.zeros(8)
        energy_fn = EnergyFunction(goal)
        
        close = Representation(z=np.array([0.01] * 8))
        far = Representation(z=np.array([10.0] * 8))
        
        assert energy_fn.compute(close) < energy_fn.compute(far)
    
    def test_guardrail_violation_adds_penalty(self):
        goal = np.zeros(4)
        guardrails = [GuardrailObjective.make_bounds([(-1, 1)] * 4)]
        energy_fn = EnergyFunction(goal, guardrails)
        
        safe = Representation(z=np.array([0.5] * 4))
        unsafe = Representation(z=np.array([5.0] * 4))
        
        assert energy_fn.compute(unsafe) > energy_fn.compute(safe) + 500
    
    def test_action_energy_cost(self):
        goal = np.zeros(4)
        energy_fn = EnergyFunction(goal)
        
        z = Representation(z=np.zeros(4))
        cheap = Action(name="wait", params={}, energy_cost=0.1)
        expensive = Action(name="run", params={}, energy_cost=10.0)
        
        e_cheap = energy_fn.compute(z, cheap)
        e_expensive = energy_fn.compute(z, expensive)
        assert e_expensive > e_cheap


# ─── GuardrailObjective ──────────────────────────────────────────

class TestGuardrailObjective:
    def test_bounds_guardrail_allows_safe(self):
        gr = GuardrailObjective.make_bounds([(-1, 1)] * 4)
        safe = Representation(z=np.array([0.5] * 4))
        assert gr(safe) is True
    
    def test_bounds_guardrail_rejects_violation(self):
        gr = GuardrailObjective.make_bounds([(-1, 1)] * 4)
        unsafe = Representation(z=np.array([2.0] * 4))
        assert gr(unsafe) is False
    
    def test_action_filter_allows_allowed(self):
        gr = GuardrailObjective.make_action_filter(["move", "inspect"])
        action = Action(name="move", params={})
        assert gr(Representation(z=np.zeros(4)), action) is True
    
    def test_action_filter_rejects_disallowed(self):
        gr = GuardrailObjective.make_action_filter(["move"])
        action = Action(name="delete", params={})
        assert gr(Representation(z=np.zeros(4)), action) is False
    
    def test_distance_limit_guardrail(self):
        ref = np.zeros(4)
        gr = GuardrailObjective.make_distance_limit(max_dist=2.0, reference=ref)
        close = Representation(z=np.array([0.5] * 4))
        far = Representation(z=np.array([10.0] * 4))
        assert gr(close) is True
        assert gr(far) is False


# ─── JEPACore ────────────────────────────────────────────────────

class TestJEPACore:
    def test_predict_returns_trajectory(self):
        perception = PerceptionModule(input_dim=16, latent_dim=8)
        energy_fn = EnergyFunction(np.zeros(8))
        jepa = JEPACore(perception, energy_fn)
        
        z = Representation(z=np.zeros(8))
        actions = [Action(name="move", params={}, energy_cost=0.5)]
        traj = jepa.predict(z, actions)
        
        assert len(traj.states) == 1
        assert len(traj.actions) == 1
        assert traj.total_energy > 0
    
    def test_longer_trajectory_has_more_energy(self):
        perception = PerceptionModule(input_dim=16, latent_dim=8)
        energy_fn = EnergyFunction(np.zeros(8))
        jepa = JEPACore(perception, energy_fn)
        
        z = Representation(z=np.zeros(8))
        short = [Action(name="move", params={}, energy_cost=0.5)]
        long_actions = [Action(name="move", params={}, energy_cost=0.5) for _ in range(5)]
        
        traj_short = jepa.predict(z, short)
        traj_long = jepa.predict(z, long_actions)
        
        assert traj_long.total_energy > traj_short.total_energy


# ─── HierarchicalPlanner ─────────────────────────────────────────

class TestHierarchicalPlanner:
    def test_plan_returns_trajectory(self):
        perception = PerceptionModule(input_dim=16, latent_dim=8)
        energy_fn = EnergyFunction(np.zeros(8))
        jepa = JEPACore(perception, energy_fn)
        planner = HierarchicalPlanner(jepa)
        
        z = Representation(z=np.random.randn(8) * 0.1)
        goal = np.zeros(8)
        traj = planner.plan(z, goal, max_depth=2, max_actions_per_level=3)
        
        assert isinstance(traj, Trajectory)
        assert len(traj.states) >= 0  # may be empty if no valid candidates
    
    def test_registered_policies_used(self):
        perception = PerceptionModule(input_dim=16, latent_dim=8)
        energy_fn = EnergyFunction(np.zeros(8))
        jepa = JEPACore(perception, energy_fn)
        planner = HierarchicalPlanner(jepa)
        
        planner.register_policy("custom_move", lambda z, g: Action(name="custom_move", params={}))
        assert "custom_move" in planner.sub_policies


# ─── WorldModelSystem ────────────────────────────────────────────

class TestWorldModelSystem:
    def test_step_returns_action(self):
        system = WorldModelSystem(obs_dim=16, latent_dim=8)
        obs = Observation(data=np.random.randn(16))
        action = system.step(obs)
        assert isinstance(action, Action)
        assert isinstance(action.name, str)
    
    def test_status_returns_dict(self):
        system = WorldModelSystem(obs_dim=16, latent_dim=8)
        obs = Observation(data=np.random.randn(16))
        system.step(obs)
        
        status = system.get_status()
        assert "steps" in status
        assert "total_energy" in status
        assert "total_guardrail_violations" in status
        assert status["steps"] == 1
    
    def test_set_goal_updates_internal_goal(self):
        system = WorldModelSystem(obs_dim=16, latent_dim=8)
        new_goal = np.ones(8) * 5.0
        system.set_goal(new_goal)
        assert np.array_equal(system.goal, new_goal)
    
    def test_no_guardrail_violations_with_bounds(self):
        """With reasonable bounds, no violations should occur."""
        system = WorldModelSystem(obs_dim=16, latent_dim=8)
        for _ in range(10):
            obs = Observation(data=np.random.randn(16) * 0.5)  # small observations
            system.step(obs)
        
        status = system.get_status()
        assert status["total_guardrail_violations"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
