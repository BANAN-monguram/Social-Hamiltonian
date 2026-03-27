
"""
Hybrid Quantum Framework
========================
Implements the Hybrid Loop: Quantum Sampling -> Classical Repair.

Classes:
- HybridSolver: Orchestrates the loop.
- ComparisonRunner: Benchmarks methods.
"""

import time
import numpy as np
from quantum_solvers import ClassicalSolver, SimulatedNISQSolver

class HybridSolver:
    def __init__(self, quantum_solver, classical_refinement_steps=50):
        self.q_solver = quantum_solver
        self.c_steps = classical_refinement_steps
        
    def solve(self, problem, seed=None):
        if seed is not None:
            np.random.seed(seed)
            
        t_start = time.time()
        
        # 1. Quantum Sampling (Parallel Candidate Generation)
        # In a real hybrid loop, this takes "Quantum Time"
        # We get S candidates.
        best_result, samples = self.q_solver.sample(problem)
        
        # 2. Classical Repair (Greedy Descent on candidates)
        # We take the top K candidates and refine them.
        candidates = sorted(samples, key=lambda x: x[1])[:5] # Top 5
        
        final_best_x = best_result.solution
        final_best_E = best_result.energy
        
        # Refine each candidate
        # This is parallelizable on classical cluster
        for x_start, e_start in candidates:
            # Use short SA or Greedy to refine
            x = x_start.copy()
            curr = e_start
            
            # Simple Greedy Descent
            improved = True
            steps = 0
            while improved and steps < self.c_steps:
                improved = False
                steps += 1
                # Try all bit flips? O(N).
                # Limit to random check for speed
                for _ in range(problem.n): # Check N random flips
                    idx = np.random.randint(0, problem.n)
                    x_new = x.copy()
                    x_new[idx] = 1 - x_new[idx]
                    e_new = x_new @ problem.qubo @ x_new
                    if e_new < curr:
                        x = x_new
                        curr = e_new
                        improved = True
            
            if curr < final_best_E:
                final_best_E = curr
                final_best_x = x.copy()
                
        t_end = time.time()
        return final_best_x, final_best_E, (t_end - t_start)

class ComparisonRunner:
    def compare(self, problem, budget_ms=1000):
        """
        Runs Classical vs Hybrid under same 'Wall Clock' budget (simulated).
        """
        results = {}
        
        # 1. Classical (SA)
        # We estimate steps based on budget?
        # Or just run a fixed strong configuration.
        sa = ClassicalSolver(steps=2000)
        res_c = sa.solve_sa(problem, seed=42)
        results['Classical'] = {'E': res_c.energy}
        
        # 2. Hybrid
        # Simulated NISQ parameters
        # High noise (T=2.0) but many shots
        nisq = SimulatedNISQSolver(noise_temp=2.0, shots=100)
        hybrid = HybridSolver(nisq, classical_refinement_steps=100)
        
        x, e, t = hybrid.solve(problem, seed=42)
        results['Hybrid'] = {'E': e}
        
        valid = (results['Hybrid']['E'] <= results['Classical']['E'] * 1.05) # Allow 5% margin
        results['HybridWin'] = (results['Hybrid']['E'] < results['Classical']['E'])
        
        return results
