import numpy as np
import random

class QuantumSolver:
    """
    Simulated Bifurcation / Annealing Solver (The Deep End).
    Match Agents <-> Tasks to minimize global mismatch.
    """
    def __init__(self, model):
        self.model = model
        
    def solve_matching(self, agents, tasks):
        """
        Returns a dictionary {task_index: agent_object}
        """
        if not tasks or not agents:
            return {}
            
        matches = {}
        # Simple heuristic annealing for simulation speed
        # In reality, this would be a QUBO solver
        
        # 1. Calculate Cost Matrix
        # Rows: Tasks, Cols: Agents
        available_agents = [a for a in agents if a.current_task is None]
        random.shuffle(available_agents)
        
        for i, task in enumerate(tasks):
            if not available_agents:
                break
            
            # Find best agent for this task (Greedy approximation of Global Opt)
            # True Quantum Solver would do this simultaneously
            best_agent = min(available_agents, key=lambda a: np.linalg.norm(a.pos - task["vec"]))
            
            matches[i] = best_agent
            available_agents.remove(best_agent)
            
        return matches
