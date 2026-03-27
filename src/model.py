from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np
from agents import HumanAgent, LLMAgent, RobotAgent
import random

class CSCTModel(Model):
    """
    A model to simulate the Computational Social Contract Theory (CSCT).
    It compares a 'Greedy' allocation strategy (Chaos/Free Market) 
    vs 'Grand Unified Algorithm' (Hamiltonian Minimization).
    """
    def __init__(self, num_humans=50, num_llms=50, num_robots=20, task_count=200):
        # Initialize parent Mesa Model (Mesa 3.x requires this for agent backend)
        super().__init__()
        
        # Mesa 3.x: model.agents is a protected property. Use a different name.
        self.agent_list = []
        self.tasks = []
        
        # Initialize Agents
        agent_id = 0
        for _ in range(num_humans):
            a = HumanAgent(agent_id, self)
            self.agent_list.append(a)
            agent_id += 1
            
        for _ in range(num_llms):
            a = LLMAgent(agent_id, self)
            self.agent_list.append(a)
            agent_id += 1
            
        for _ in range(num_robots):
            a = RobotAgent(agent_id, self)
            self.agent_list.append(a)
            agent_id += 1
            
        # Initialize Tasks
        self.generate_tasks(task_count)
        
        self.datacollector = DataCollector(
            model_reporters={"Hamiltonian": "hamiltonian"}
        )
        
        self.hamiltonian = 0.0

    def generate_tasks(self, count):
        """Generate a random set of tasks."""
        task_types = ['Logic', 'Creative', 'Physical']
        self.tasks = []
        for i in range(count):
            t_type = np.random.choice(task_types, p=[0.4, 0.4, 0.2])
            difficulty = np.random.random()
            self.tasks.append({
                'id': i,
                'type': t_type,
                'difficulty': difficulty,
                'assigned_to': None
            })

    def calculate_hamiltonian(self, assignments):
        """
        Calculate the Social Hamiltonian H for a given assignment configuration.
        H = E_sys (Costs + Mismatches) - lambda * W_human (Well-being)
        """
        total_cost = 0.0
        total_wellbeing = 0.0
        
        for task_idx, agent_idx in assignments.items():
            if agent_idx is None:
                total_cost += 50.0 # High penalty for unassigned task
                continue
                
            task = self.tasks[task_idx]
            # Find agent by ID (optimized lookup would be better but list is small)
            agent = next((a for a in self.agent_list if a.unique_id == agent_idx), None)
            if not agent: continue

            # 1. Base Cost
            total_cost += agent.cost_per_tick
            
            # 2. Capability Mismatch Penalty
            capability = 0.0
            if task['type'] == 'Logic': capability = agent.logic
            elif task['type'] == 'Creative': capability = agent.creativity
            elif task['type'] == 'Physical': capability = agent.physical
            
            if task['difficulty'] > capability:
                total_cost += (task['difficulty'] - capability) * 20.0 # Penalty
                
            # Physical task constraint for LLM
            if task['type'] == 'Physical' and agent.agent_type == 'LLM':
                total_cost += 1000.0 # Impossible
                
            # 3. Human Well-being (Negative Energy)
            if agent.agent_type == 'Human':
                # Humans like Creative work, dislike rote Logic if mismatch
                if task['type'] == 'Creative':
                    total_wellbeing += 10.0
                elif task['type'] == 'Logic' and task['difficulty'] > 0.8:
                    total_wellbeing -= 5.0 # Stress
                    
        # H = Cost - Well-being
        H = total_cost - total_wellbeing
        return H

    def run_allocation_greedy(self):
        """Baseline: Assign tasks randomly/greedily to first available agent."""
        assignments = {}
        available_agents = [a.unique_id for a in self.agent_list]
        np.random.shuffle(available_agents)
        
        agent_ptr = 0
        for i, task in enumerate(self.tasks):
            if agent_ptr < len(available_agents):
                assignments[i] = available_agents[agent_ptr]
                agent_ptr += 1
            else:
                assignments[i] = None # No agents left
                
        self.hamiltonian = self.calculate_hamiltonian(assignments)
        return self.hamiltonian

    def run_allocation_optimized(self):
        """
        Deep End: Optimize allocation to minimize Hamiltonian.
        Simplified Greedy-Best-First approach for demonstration.
        """
        assignments = {}
        # Reset agents busy state
        for a in self.agent_list: a.is_busy = False
        
        # Sort tasks by difficulty (descending) - heuristic
        sorted_tasks = sorted(enumerate(self.tasks), key=lambda x: x[1]['difficulty'], reverse=True)
        
        for task_idx, task in sorted_tasks:
            best_agent_idx = None
            min_local_h = float('inf')
            
            # Find best agent for this task
            for agent in self.agent_list:
                if agent.is_busy: continue
                
                # Calculate local H delta
                # Cost
                cost = agent.cost_per_tick
                
                # Mismatch
                capability = 0.0
                if task['type'] == 'Logic': capability = agent.logic
                elif task['type'] == 'Creative': capability = agent.creativity
                elif task['type'] == 'Physical': capability = agent.physical
                
                mismatch = 0.0
                if task['difficulty'] > capability:
                    mismatch = (task['difficulty'] - capability) * 20.0
                
                if task['type'] == 'Physical' and agent.agent_type == 'LLM':
                    mismatch = 1000.0
                    
                # Well-being
                wellbeing = 0.0
                if agent.agent_type == 'Human':
                    if task['type'] == 'Creative': wellbeing = 10.0
                    elif task['type'] == 'Logic' and task['difficulty'] > 0.8: wellbeing = -5.0
                
                local_h = cost + mismatch - wellbeing
                
                if local_h < min_local_h:
                    min_local_h = local_h
                    best_agent_idx = agent.unique_id
            
            if best_agent_idx is not None:
                assignments[task_idx] = best_agent_idx
                # Mark agent busy
                agent = next(a for a in self.agent_list if a.unique_id == best_agent_idx)
                agent.is_busy = True
            else:
                assignments[task_idx] = None
        
        self.hamiltonian = self.calculate_hamiltonian(assignments)
        return self.hamiltonian
    
    def step(self):
        """Advance the model by one step."""
        random.shuffle(self.agent_list)
        for agent in self.agent_list:
            agent.step()

