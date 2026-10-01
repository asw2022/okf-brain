"""
JEPA World Model — Reference Implementation
Based on Yann LeCun's NYU talk (2026-09-30):
"Predict in representation space, not pixel space.
Optimize energy, don't autoregress."

Core idea: Intelligence = ability to learn quickly + predict
consequences + plan with guardrails.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Tuple
import json


# ─── Data Structures ────────────────────────────────────────────

@dataclass
class Observation:
    """Raw sensory input from the environment."""
    data: np.ndarray          # raw observation (pixels, sensor readings, etc.)
    timestamp: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class Representation:
    """Abstract embedding of observed state — predictable part only."""
    z: np.ndarray             # latent representation
    predictable: bool = True  # was this predictable? (JEPA eliminates unpredictable info)
    confidence: float = 1.0   # prediction confidence


@dataclass
class Action:
    """System action in the environment."""
    name: str
    params: dict = field(default_factory=dict)
    energy_cost: float = 0.0


@dataclass
class Trajectory:
    """Sequence of (representation, action) pairs."""
    states: List[Representation] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    total_energy: float = 0.0
    guardrail_violations: int = 0


# ─── Core Modules ───────────────────────────────────────────────

class PerceptionModule:
    """
    Encodes raw observations into abstract representations.
    
    In LeCun's vision: learns what is predictable about the world.
    Unpredictable details (e.g. which chair is where) are discarded.
    Only structural/physical regularities are kept.
    """
    
    def __init__(self, input_dim: int, latent_dim: int = 128):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        # Random projection for demo; real system would be learned
        self.W_enc = np.random.randn(input_dim, latent_dim) * 0.01
        self.bias = np.zeros(latent_dim)
    
    def encode(self, obs: Observation) -> Representation:
        """Encode observation → latent representation."""
        z = np.tanh(obs.data @ self.W_enc + self.bias)
        return Representation(z=z, predictable=True, confidence=0.9)
    
    def predict_next(self, z_current: Representation, action: Action) -> Representation:
        """
        JEPA prediction: given current representation + action,
        predict next representation in abstract space.
        
        NOT pixel-level reconstruction. Only predictable structure.
        """
        # Simple linear dynamics for demo; real JEPA would be a learned model
        action_enc = np.zeros(self.latent_dim)
        action_hash = hash(action.name) % (2 ** 16)
        action_enc[0] = action_hash / (2 ** 16)
        
        z_next = z_current.z * 0.9 + action_enc * 0.1 + np.random.randn(self.latent_dim) * 0.01
        return Representation(z=np.tanh(z_next), predictable=True, confidence=0.85)


class EnergyFunction:
    """
    Scalar energy landscape: E(state, goal) → ℝ.
    Lower energy = more compatible with goal.
    
    This is the "objective" LeCun describes — not a loss to minimize
    during training, but an inference-time objective to search.
    """
    
    def __init__(self, goal: np.ndarray, guardrails: Optional[List[Callable]] = None):
        self.goal = goal                    # target representation
        self.guardrails = guardrails or []  # safety constraints
    
    def compute(self, z: Representation, action: Optional[Action] = None) -> float:
        """Energy of a state (lower = better)."""
        # Distance to goal in representation space
        goal_dist = float(np.linalg.norm(z.z - self.goal))
        
        # Guardrail violations add infinite energy (hard constraints)
        violation_penalty = 0.0
        for gr in self.guardrails:
            result = gr(z, action)
            if result is not None and not result:
                violation_penalty += 1000.0  # hard constraint violation
        
        # Action energy cost
        action_cost = action.energy_cost if action else 0.0
        
        return goal_dist + violation_penalty + action_cost * 0.1


class GuardrailObjective:
    """
    Safety constraints as part of the energy landscape.
    
    Key insight from LeCun: guardrails are OPTIMIZED, not filtered.
    The system cannot output unsafe states because they have high energy.
    This is fundamentally different from LLM safety (fine-tuning/filtering).
    """
    
    @staticmethod
    def make_bounds(bounds: List[Tuple[float, float]]) -> Callable:
        """Create a bound guardrail: each dim must stay within [min, max]."""
        def guardrail(z: Representation, action: Optional[Action] = None) -> bool:
            for i, (lo, hi) in enumerate(bounds):
                if i < len(z.z) and (z.z[i] < lo or z.z[i] > hi):
                    return False
            return True
        return guardrail
    
    @staticmethod
    def make_distance_limit(max_dist: float, reference: np.ndarray) -> Callable:
        """State must stay within max_dist of reference point."""
        def guardrail(z: Representation, action: Optional[Action] = None) -> bool:
            return float(np.linalg.norm(z.z - reference)) <= max_dist
        return guardrail
    
    @staticmethod
    def make_action_filter(allowed_actions: List[str]) -> Callable:
        """Only allowed actions are valid."""
        def guardrail(z: Representation, action: Optional[Action] = None) -> bool:
            if action is None:
                return True
            return action.name in allowed_actions
        return guardrail


# ─── JEPA Core ──────────────────────────────────────────────────

class JEPACore:
    """
    Joint Embedding Predictive Architecture.
    
    Predicts future representations, NOT pixel reconstruction.
    Eliminates unpredictable information from the representation.
    """
    
    def __init__(self, perception: PerceptionModule, energy_fn: EnergyFunction):
        self.perception = perception
        self.energy_fn = energy_fn
        self.history: List[Representation] = []
    
    def predict(self, z_current: Representation, actions: List[Action]) -> Trajectory:
        """
        Simulate action sequence through world model.
        Returns trajectory with predicted states + total energy.
        """
        traj = Trajectory()
        z = z_current
        
        for action in actions:
            # Predict next state in representation space
            z_next = self.perception.predict_next(z, action)
            
            # Compute energy for this step
            step_energy = self.energy_fn.compute(z_next, action)
            
            traj.states.append(z_next)
            traj.actions.append(action)
            traj.total_energy += step_energy
            
            # Check guardrails
            for gr in self.energy_fn.guardrails:
                if gr(z_next, action) is not None and not gr(z_next, action):
                    traj.guardrail_violations += 1
            
            z = z_next
        
        return traj


# ─── Hierarchical Planner ───────────────────────────────────────

class HierarchicalPlanner:
    """
    Multi-level planning as LeCun describes:
    
    Level 0: Muscle actions (specific motor commands)
    Level 1: Skills (drive to airport, pick up object)
    Level 2: Tasks (go to Paris, cook dinner)
    Level 3: Goals (why am I doing this?)
    
    Each level plans at its own abstraction.
    Lower levels are treated as policies (learned).
    Higher levels use the world model + energy optimization.
    """
    
    def __init__(self, jepa: JEPACore):
        self.jepa = jepa
        self.sub_policies: dict[str, Callable] = {}  # name → policy function
    
    def register_policy(self, name: str, policy_fn: Callable):
        """Register a sub-policy for a skill/action."""
        self.sub_policies[name] = policy_fn
    
    def plan(self,
             z_initial: Representation,
             goal_z: np.ndarray,
             max_depth: int = 3,
             max_actions_per_level: int = 5) -> Trajectory:
        """
        Hierarchical planning:
        1. Define high-level goal (target representation)
        2. Generate candidate action sequences at top level
        3. For each candidate, simulate through world model
        4. Select sequence with lowest energy
        5. Recursively decompose sub-goals
        """
        energy_fn = self.jepa.energy_fn
        
        # Generate candidate action sequences
        candidates = self._generate_candidates(
            z_initial, goal_z, max_actions_per_level
        )
        
        # Evaluate each candidate through world model
        best_traj = None
        best_energy = float('inf')
        
        for actions in candidates:
            traj = self.jepa.predict(z_initial, actions)
            
            # Final state energy (primary objective)
            final_energy = energy_fn.compute(traj.states[-1] if traj.states else z_initial)
            
            # Guardrail penalty
            final_energy += traj.guardrail_violations * 500.0
            
            if final_energy < best_energy and traj.guardrail_violations == 0:
                best_energy = final_energy
                best_traj = traj
        
        return best_traj or Trajectory(states=[z_initial])
    
    def _generate_candidates(self, z_init: Representation, goal: np.ndarray, n: int) -> List[List[Action]]:
        """Generate candidate action sequences (random exploration for demo)."""
        candidates = []
        action_pool = list(self.sub_policies.keys()) or ["move", "wait", "inspect"]
        
        for _ in range(n):
            length = np.random.randint(1, 5)
            actions = []
            for _ in range(length):
                name = action_pool[np.random.randint(len(action_pool))]
                actions.append(Action(name=name, params={}, energy_cost=np.random.uniform(0.1, 1.0)))
            candidates.append(actions)
        
        return candidates


# ─── Full System ────────────────────────────────────────────────

class WorldModelSystem:
    """
    Complete JEPA-based world model system.
    
    Pipeline:
    1. Observe → PerceptionModule → Representation
    2. Generate candidate actions
    3. JEPA predicts outcomes in representation space
    4. Energy function evaluates each trajectory
    5. Guardrails enforce safety as hard constraints
    6. Hierarchical planner decomposes complex goals
    7. Execute best action → observe → repeat
    """
    
    def __init__(self, obs_dim: int, latent_dim: int = 128, goal: Optional[np.ndarray] = None):
        self.perception = PerceptionModule(obs_dim, latent_dim)
        self.goal = goal or np.zeros(latent_dim)
        
        guardrails = [
            GuardrailObjective.make_bounds([(-2.0, 2.0)] * latent_dim),
        ]
        energy_fn = EnergyFunction(self.goal, guardrails)
        
        self.jepa = JEPACore(self.perception, energy_fn)
        self.planner = HierarchicalPlanner(self.jepa)
        self.history: List[Trajectory] = []
    
    def set_goal(self, goal_z: np.ndarray):
        """Update the goal representation."""
        self.goal = goal_z
        self.jepa.energy_fn.goal = goal_z
    
    def step(self, obs: Observation) -> Action:
        """
        One planning-execution cycle:
        1. Encode observation
        2. Plan best action sequence
        3. Return first action to execute
        """
        z = self.perception.encode(obs)
        traj = self.planner.plan(z, self.goal)
        
        if traj.actions:
            best_action = traj.actions[0]
        else:
            best_action = Action(name="wait", params={})
        
        # Record trajectory
        self.history.append(traj)
        
        return best_action
    
    def get_status(self) -> dict:
        """System status for monitoring."""
        total_violations = sum(t.guardrail_violations for t in self.history)
        total_energy = sum(t.total_energy for t in self.history)
        
        return {
            "steps": len(self.history),
            "total_energy": total_energy,
            "total_guardrail_violations": total_violations,
            "avg_energy_per_step": total_energy / max(len(self.history), 1),
            "goal_distance": float(np.linalg.norm(
                self.history[-1].states[-1].z - self.goal
            )) if self.history and self.history[-1].states else None,
        }
