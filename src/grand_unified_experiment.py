
"""
Grand Unified Experiment
========================
Tests G-Claim-1/2/3: The stability and convergence of the Outer Loop.
Integrates Trust Dynamics + Quantum Local Optimization.

Classes:
- OuterLoopSystem: The macro-system state (J, tau).
- CSCTController: System 2 Controller.
"""

import numpy as np
from quantum_benchmarks import BenchmarkGenerator
from hybrid_engine import HybridSolver, ComparisonRunner
from quantum_solvers import SimulatedNISQSolver

class CSCTController:
    """
    Implements Spec 2.5.8 (CSCT Drive)
    Outputs control signals based on Macro State.
    """
    def __init__(self):
        self.history_F = []
        
    def get_control(self, current_F, entropy):
        # Damping Control: If F is oscillating, increase damping.
        self.history_F.append(current_F)
        
        damping = 0.1 # Default learning rate
        if len(self.history_F) > 5:
            # Check oscillation: sign changes in delta
            deltas = np.diff(self.history_F[-5:])
            sign_changes = np.sum(np.diff(np.sign(deltas)) != 0)
            if sign_changes > 2:
                damping *= 0.5 # Slow down
                
        # Safety Clip
        clip_norm = 1.0
        
        return {'damping': damping, 'clip': clip_norm}

class OuterLoopSystem:
    def __init__(self, n_agents=50, comparison_mode=False):
        self.n = n_agents
        np.random.seed(42)
        
        # State
        self.tau = np.random.uniform(0.1, 0.5, n_agents) # Trust
        self.J = np.random.uniform(-0.1, 0.1, (n_agents, n_agents)) # Coupling (Dense for simplicity in proto)
        self.J = (self.J + self.J.T)/2 # Symmetric
        
        # Sub-components
        self.controller = CSCTController()
        self.bench_gen = BenchmarkGenerator()
        
        # Solver (Hybrid)
        nisq = SimulatedNISQSolver(noise_temp=1.5, shots=50)
        self.hybrid = HybridSolver(nisq, classical_refinement_steps=20)
        
        self.comparison_mode = comparison_mode
        self.mode_classical_only = False
        
        # Metrics
        self.log_F = []
        self.log_Trust = []
        
    def calculate_free_energy(self):
        # F = <H> - T<S> approx
        # Simplified: F = Sum(Mismatch) - Sum(Trust * Activity)
        # Here we define a toy potential for demonstration
        # F = (1/2) x^T J x ... but we don't have global x.
        # We define F as "System Frustration"
        # Frustration = Sum |J_ij| (if unsatisfied) 
        # But J evolves.
        
        # Let's use specific proxy: 
        # F = (sum of all current local max-cut violations) - (mean trust)
        energy_term = np.sum(np.abs(self.J)) # Energy stored in bonds
        trust_term = np.sum(self.tau)
        return energy_term - trust_term # Min F => Low Bond Stress, High Trust

    def step(self, t):
        # 1. Observation
        F = self.calculate_free_energy()
        self.log_F.append(F)
        self.log_Trust.append(np.mean(self.tau))
        
        # 2. Controller
        ctrl = self.controller.get_control(F, 0)
        eta = ctrl['damping']
        
        # 3. Tokenized Work / Trust Update (Spec 2.5.9)
        # Simulate work events: Agents interacting
        # Successful interaction -> Trust ++
        # In comparison mode, maybe this is static.
        
        # Random interactions
        pairs = np.random.randint(0, self.n, (10, 2))
        for i, j in pairs:
            if i == j: continue
            # Success prob depends on Trust
            prob = (self.tau[i] + self.tau[j])/2
            if np.random.random() < prob:
                self.tau[i] = min(1.0, self.tau[i] + 0.01)
                self.tau[j] = min(1.0, self.tau[j] + 0.01)
            else:
                self.tau[i] *= 0.99
                self.tau[j] *= 0.99
                
        # 4. Local Optimization (J Update) - The Quantum Part
        # Pick a cluster (random subgraph)
        indices = np.random.choice(self.n, 20, replace=False) # N=20 Subproblem
        
        # Create Max-Cut instance for this subgraph
        # Weights = current J_ij (we want to Optimize J to minimize stress?)
        # Or J is the solution?
        # In the theory: We update J to minimize H. 
        # Here: We solve MaxCut on the subgraph to find "Optimal Configuration s"
        # Then we update J to reinforce this configuration (Hebbian).
        # J_new = J + eta * (s_i * s_j)
        
        # Extract subgraph interactions as QUBO
        # Problem: Find `s` that agrees with `J` (Min Energy)
        # Flip sign of J for QUBO (since QUBO minimizes)
        # If J_ij > 0 (ferro), we want s_i = s_j. 
        # If J_ij < 0 (anti), we want s_i != s_j.
        
        # Construct simplified QUBO for the solver
        # We generate a "Task" that requires optimization.
        # Benchmark Generator used here just for structure
        # But we need specific weights.
        
        sub_Q = np.zeros((20, 20))
        for idx_i, node_i in enumerate(indices):
            for idx_j, node_j in enumerate(indices):
                if idx_i <= idx_j: continue
                weight = self.J[node_i, node_j]
                # Map to QUBO
                sub_Q[idx_i, idx_j] = weight
        
        # Create Problem Object
        class SubProb:
            def __init__(self, q): self.qubo = q; self.n = 20
        
        prob = SubProb(sub_Q)
        
        # SOLVE
        # If comparison mode A (Classical)
        if self.mode_classical_only:
             # Basic greedy or SA
             # Mock result
             s_opt = np.random.randint(0, 2, 20) 
        else:
             # Hybrid
             s_opt, _, _ = self.hybrid.solve(prob)
             
        # 5. Update J (Hebbian Learning / Optimization)
        # J_ij += eta * (2*s_i - 1) * (2*s_j - 1)
        # This aligns the social structure with the "Optimal State" found by Quantum
        
        for idx_i, node_i in enumerate(indices):
            for idx_j, node_j in enumerate(indices):
                if idx_i == idx_j: continue
                spin_i = 2*s_opt[idx_i] - 1
                spin_j = 2*s_opt[idx_j] - 1
                
                delta = eta * spin_i * spin_j
                self.J[node_i, node_j] += delta
                
                # Decay (Regularization)
                self.J[node_i, node_j] *= 0.99
                
                # Clip
                self.J[node_i, node_j] = np.clip(self.J[node_i, node_j], -1.0, 1.0)

    def run(self, steps=100):
        for t in range(steps):
            self.step(t)
        return self.log_F, self.log_Trust
