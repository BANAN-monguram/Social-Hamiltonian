
"""
Quantum Experiment Solvers
==========================
Solvers for QUBO problems.

Classes:
- ClassicalSolver: Standard Simulated Annealing (SA).
- SimulatedNISQSolver: Noisy Thermal Sampling proxy for NISQ devices.
"""

import numpy as np

class SolverResult:
    def __init__(self, solution, energy, time_taken=0.0):
        self.solution = solution # binary array
        self.energy = energy
        self.time_taken = time_taken

class ClassicalSolver:
    def __init__(self, steps=1000):
        self.steps = steps

    def solve_sa(self, problem, seed=None):
        """Simulated Annealing"""
        if seed is not None:
            np.random.seed(seed)
            
        N = problem.n
        Q = problem.qubo
        
        # Initial State
        x = np.random.randint(0, 2, N)
        current_E = x @ Q @ x
        best_x = x.copy()
        best_E = current_E
        
        T_start = 10.0
        T_end = 0.1
        
        for i in range(self.steps):
            T = T_start * ((T_end / T_start) ** (i / self.steps))
            
            # Bit flip
            idx = np.random.randint(0, N)
            
            # Delta E calculation (optimized)
            # x_new = x_old + delta_x (where delta_x is +1 or -1 at idx)
            # new_val = 1 - current_val
            # Efficient update: Delta = (1-2x_i) * (2 * (Q[i] @ x) + Q[i,i] * (1-2x_i)) ... simplified logic needed
            
            # Simple full recalc for robustness in proto
            x_new = x.copy()
            x_new[idx] = 1 - x_new[idx]
            new_E = x_new @ Q @ x_new
            
            delta = new_E - current_E
            
            if delta < 0 or np.random.random() < np.exp(-delta / T):
                x = x_new
                current_E = new_E
                
                if current_E < best_E:
                    best_E = current_E
                    best_x = x.copy()
                    
        return SolverResult(best_x, best_E)

class SimulatedNISQSolver:
    """
    Simulates a NISQ device using 'Noisy Thermal Sampling'.
    NISQ devices (like QAOA) ideally sample from a distribution concentrated near the optimum.
    Real noise flattens this distribution.
    
    Proxy Model: Samples from Gibbs distribution exp(-E / T_noise)
    where T_noise represents the 'Noise Level' (gate errors).
    """
    def __init__(self, noise_temp=1.0, shots=100):
        self.noise_temp = noise_temp
        self.shots = shots
        
    def sample(self, problem, seed=None):
        """
        Returns a list of (solution, energy) tuples.
        """
        if seed is not None:
            np.random.seed(seed)
            
        # We model the NISQ output distribution directly using MCMC
        # Warning: For large N, we cannot compute the full partition function.
        # So we run parallel MCMC chains to generate samples.
        # This acts as a 'physical simulation' of the quantum process.
        
        N = problem.n
        Q = problem.qubo
        samples = []
        
        # Number of parallel chains? MCMC is classical, so sequential generation.
        # To simulate 'Instant' quantum sampling, we don't count the MCMC steps in 'Classical Runtime' budget usually,
        # but here we just need the OUTPUTS.
        
        # We run a short MCMC chain for each shot to get a sample
        # The chain length represents 'Circuit Depth' (mixing time).
        chain_length = N * 2 
        
        for _ in range(self.shots):
            x = np.random.randint(0, 2, N)
            curr_E = x @ Q @ x
            
            for _ in range(chain_length):
                idx = np.random.randint(0, N)
                x_new = x.copy()
                x_new[idx] = 1 - x_new[idx]
                new_E = x_new @ Q @ x_new
                delta = new_E - curr_E
                
                # Metropolis at T_noise
                if delta < 0 or np.random.random() < np.exp(-delta / self.noise_temp):
                    x = x_new
                    curr_E = new_E
            
            samples.append((x, curr_E))
            
        # Return best
        best_x, best_E = min(samples, key=lambda item: item[1])
        return SolverResult(best_x, best_E), samples
