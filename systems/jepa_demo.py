"""
JEPA World Model — Interactive Demo
Run: python jepa_demo.py

Shows the full pipeline:
1. Perception encodes observation → representation
2. JEPA predicts future states for candidate actions
3. Energy function evaluates trajectories
4. Guardrails filter unsafe options
5. Hierarchical planner selects best action
"""

import numpy as np
from jepa_world_model import (
    Observation, Action, PerceptionModule, EnergyFunction,
    GuardrailObjective, JEPACore, HierarchicalPlanner, WorldModelSystem, Representation
)


def demo_basic_prediction():
    """Show JEPA predicting in representation space."""
    print("=" * 60)
    print("JEPA WORLD MODEL — Basic Prediction Demo")
    print("=" * 60)
    
    # Setup
    obs_dim = 64
    latent_dim = 32
    system = WorldModelSystem(obs_dim, latent_dim)
    
    # Set a goal (target representation)
    goal = np.random.randn(latent_dim) * 0.5
    system.set_goal(goal)
    print(f"\nGoal set: {goal[0]:.3f}, {goal[1]:.3f}, ... ({latent_dim} dims)")
    
    # Simulate observations
    for step in range(5):
        obs_data = np.random.randn(obs_dim) * 0.3 + step * 0.1
        obs = Observation(data=obs_data, timestamp=step * 0.1)
        
        # Encode
        z = system.perception.encode(obs)
        print(f"\nStep {step}: |z| = {np.linalg.norm(z.z):.3f}, confidence = {z.confidence:.2f}")
        
        # Plan
        action = system.step(obs)
        print(f"  → Action: {action.name} (energy_cost={action.energy_cost:.2f})")
    
    status = system.get_status()
    print(f"\n--- Status ---")
    print(f"Steps: {status['steps']}")
    print(f"Total energy: {status['total_energy']:.3f}")
    print(f"Guardrail violations: {status['total_guardrail_violations']}")
    print(f"Avg energy/step: {status['avg_energy_per_step']:.3f}")
    print(f"Goal distance: {status['goal_distance']:.3f}" if status['goal_distance'] else "Goal distance: N/A")


def demo_guardrails():
    """Show guardrails as hard constraints in energy landscape."""
    print("\n" + "=" * 60)
    print("GUARDRAILS — Safety as Energy Constraint")
    print("=" * 60)
    
    latent_dim = 16
    
    # Goal far away
    goal = np.array([5.0] * latent_dim)
    
    # Guardrail: state must stay within bounds [-2, 2]
    guardrails = [
        GuardrailObjective.make_bounds([(-2.0, 2.0)] * latent_dim),
    ]
    
    energy_fn = EnergyFunction(goal, guardrails)
    
    # Test states
    safe_state = Representation(z=np.array([0.5] * latent_dim))
    unsafe_state = Representation(z=np.array([3.0] * latent_dim))
    
    safe_energy = energy_fn.compute(safe_state)
    unsafe_energy = energy_fn.compute(unsafe_state)
    
    print(f"\nSafe state  {safe_state.z[:3]}...  → Energy: {safe_energy:.3f}")
    print(f"Unsafe state {unsafe_state.z[:3]}... → Energy: {unsafe_energy:.3f}")
    print(f"→ Guardrail penalty: {unsafe_energy - safe_energy:.0f}x higher")
    
    # Show that guardrail-violating actions get rejected
    action = Action(name="move", params={}, energy_cost=1.0)
    
    for gr in guardrails:
        result = gr(safe_state, action)
        print(f"\nGuardrail check (safe): {result}")
        result = gr(unsafe_state, action)
        print(f"Guardrail check (unsafe): {result}")


def demo_hierarchical_planning():
    """Show hierarchical planning decomposition."""
    print("\n" + "=" * 60)
    print("HIERARCHICAL PLANNING — Goal Decomposition")
    print("=" * 60)
    
    obs_dim = 32
    latent_dim = 16
    system = WorldModelSystem(obs_dim, latent_dim)
    
    # Register sub-policies (skills)
    system.planner.register_policy("move_to", lambda z, g: Action(name="move", params={"target": "goal"}))
    system.planner.register_policy("inspect", lambda z, g: Action(name="inspect", params={}))
    system.planner.register_policy("wait", lambda z, g: Action(name="wait", params={}))
    system.planner.register_policy("open_door", lambda z, g: Action(name="open_door", params={}))
    
    # Goal: representations that are "at destination"
    goal = np.random.randn(latent_dim) * 0.3
    system.set_goal(goal)
    
    # Run hierarchical planning
    obs = Observation(data=np.random.randn(obs_dim), timestamp=0.0)
    z = system.perception.encode(obs)
    
    print(f"\nInitial state |z| = {np.linalg.norm(z.z):.3f}")
    print(f"Goal       |z| = {np.linalg.norm(goal):.3f}")
    
    traj = system.planner.plan(z, goal, max_depth=3, max_actions_per_level=8)
    
    print(f"\nPlanned trajectory:")
    print(f"  Actions: {[a.name for a in traj.actions]}")
    print(f"  Total energy: {traj.total_energy:.3f}")
    print(f"  States predicted: {len(traj.states)}")
    print(f"  Guardrail violations: {traj.guardrail_violations}")


def demo_jepa_vs_autoregressive():
    """Contrast JEPA approach with autoregressive LLM approach."""
    print("\n" + "=" * 60)
    print("JEPA vs Autoregressive — Key Difference")
    print("=" * 60)
    
    latent_dim = 16
    perception = PerceptionModule(input_dim=32, latent_dim=latent_dim)
    
    # Simulate an observation
    obs = Observation(data=np.random.randn(32))
    z = perception.encode(obs)
    
    action = Action(name="move_forward", params={}, energy_cost=0.5)
    
    # JEPA: predict next representation directly
    z_next_jepa = perception.predict_next(z, action)
    print(f"\nJEPA prediction:")
    print(f"  Input |z|  = {np.linalg.norm(z.z):.3f}")
    print(f"  Output|z'| = {np.linalg.norm(z_next_jepa.z):.3f}")
    print(f"  Predicts STRUCTURE (what changes), not pixels")
    
    # Energy-based evaluation
    goal = np.random.randn(latent_dim) * 0.2
    energy_fn = EnergyFunction(goal)
    e = energy_fn.compute(z_next_jepa, action)
    print(f"  Energy: {e:.3f} (lower = closer to goal)")
    
    print(f"\nAutoregressive LLM (contrast):")
    print(f"  Predicts next TOKEN in sequence")
    print(f"  No world model, no energy function")
    print(f"  Cannot answer: 'what happens if I push this?'")
    
    print(f"\nKey insight: JEPA eliminates unpredictable info")
    print(f"(e.g., exact pixel details) from representation.")
    print(f"Only keeps what matters for the task.")


if __name__ == "__main__":
    print("\n🧠 JEPA WORLD MODEL — Reference Implementation")
    print("   Based on Yann LeCun NYU Talk (2026-09-30)")
    print("   'Predict in representation space, not pixel space'\n")
    
    demo_basic_prediction()
    demo_guardrails()
    demo_hierarchical_planning()
    demo_jepa_vs_autoregressive()
    
    print("\n" + "=" * 60)
    print("All demos complete.")
    print("=" * 60)
