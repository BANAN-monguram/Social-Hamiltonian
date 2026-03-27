from mesa import Model
from mesa.datacollection import DataCollector
from agents import HumanAgent, LLMAgent, RobotAgent # Reuse existing agents
import networkx as nx
import numpy as np
import random

class MacroCSCTModel(Model):
    """
    Phase 2 Model: Macro Behavior & Trust Network.
    Simulates how 'Trust' acts as a buffer against 'Work Volatility'.
    """
    def __init__(self, num_humans=50, num_llms=50, num_robots=10):
        super().__init__()
        self.agent_list = []
        self.G = nx.Graph() # Trust Network
        
        # 1. Initialize Agents
        agent_id = 0
        for _ in range(num_humans):
            a = HumanAgent(agent_id, self)
            a.current_load = 0.0 # Add dynamic property for Volatility Model
            a.base_capacity = 1.0
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="Human")
            agent_id += 1
            
        for _ in range(num_llms):
            a = LLMAgent(agent_id, self)
            a.current_load = 0.0
            a.base_capacity = 5.0
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="LLM")
            agent_id += 1
            
        for _ in range(num_robots):
            a = RobotAgent(agent_id, self)
            a.current_load = 0.0
            a.base_capacity = 3.0
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="Robot")
            agent_id += 1
            
        # 2. Initialize Trust Network (Scale-free network mostly Humans)
        # Humans tend to cluster. LLMs/Robots are tools attached to humans or central nodes.
        self._build_initial_network()
        
        self.volatility_index = 0.0 # Current system volatility
        self.total_trust = 0.0
        
        self.datacollector = DataCollector(
            model_reporters={
                "Volatility": "volatility_index",
                "TotalTrust": "total_trust",
                "CompletedTasks": "completed_tasks_count",
                "Hamiltonian": "current_hamiltonian"
            }
        )
        self.completed_tasks_count = 0
        self.current_hamiltonian = 0.0

    def _build_initial_network(self):
        """Build a random geometric graph or scale-free graph for humans."""
        # For simplicity, random connection with higher probability for Humans
        for agent in self.agent_list:
            # Connect to k random other agents
            k = 3
            targets = random.sample(self.agent_list, k)
            for target in targets:
                if agent.unique_id == target.unique_id: continue
                
                # Trust Level (Weight)
                # Human-Human: High Trust potential
                # Human-LLM: Medium (Tool reliance)
                weight = 0.1
                if agent.agent_type == 'Human' and target.agent_type == 'Human':
                    weight = 0.5
                elif agent.agent_type == 'Human' and target.agent_type == 'LLM':
                    weight = 0.8 # Humans trust tools to work
                    
                if not self.G.has_edge(agent.unique_id, target.unique_id):
                    self.G.add_edge(agent.unique_id, target.unique_id, weight=weight)

    def generate_volatility_shock(self):
        """Introduce a sudden burst of tasks (Work Volatility)."""
        # Random shock: A burst of work lands on specific nodes (e.g. popular creators or central nodes)
        if random.random() < 0.15: # 15% shock chance
            magnitude = random.randint(20, 100)
            
            # Target random agents (Shock is local, propagation is global)
            target = random.choice(self.agent_list)
            target.current_load += magnitude            


    def calculate_hamiltonian(self):
        """
        Calculate Social Hamiltonian H (Eq. 160 in Thesis).
        H = Sum(Skill_Mismatch^2) - gamma * Sum(Wellbeing)
        """
        bias_mismatch = 0.0
        total_wellbeing = 0.0
        gamma = 1.0 # Wellbeing weight
        
        for agent in self.agent_list:
            # Simplified match quality based on current 'load' or 'volatility' being processed
            # If agent is overwhelmed (volatility > capacity), that is a mismatch.
            capacity = agent.base_capacity
            load = agent.current_load
            
            if load > capacity:
                mismatch = (load - capacity) ** 2 # Quadratic penalty for overload
                bias_mismatch += mismatch
                agent.stress += 0.1
            else:
                # Proper match
                agent.stress = max(0, agent.stress - 0.05)
                
            # Wellbeing accumulation
            if agent.agent_type == 'Human':
                # Humans gain wellbeing if load is balanced (Flow state)
                if 0.5 * capacity < load <= capacity:
                    total_wellbeing += 1.0
                    agent.well_being += 0.1
                elif load > capacity:
                    total_wellbeing -= 1.0 # Burnout
                    agent.well_being -= 0.1
                    
        return bias_mismatch - gamma * total_wellbeing

    def step(self):
        # 1. Volatility Shock (External Demand)
        self.generate_volatility_shock()
        
        # 2. Distribute Volatility via Trust Network
        # Tasks flow from high-load nodes to low-load neighbors via Trust links
        # (Simplified diffusion process)
        for _ in range(3): # Run a few diffusion steps per tick
            for agent in self.agent_list:
                neighbors = list(self.G.neighbors(agent.unique_id))
                if not neighbors: continue
                
                # Check neighbors who have less load
                my_load = agent.current_load
                
                for neighbor_id in neighbors:
                    neighbor = self.get_agent(neighbor_id)
                    if not neighbor: continue
                    
                    # Diffusion gradient
                    if my_load > neighbor.current_load:
                        # Flow rate depends on Trust (Edge Weight)
                        trust = self.G[agent.unique_id][neighbor_id]['weight']
                        flow = (my_load - neighbor.current_load) * 0.5 * trust
                        
                        agent.current_load -= flow
                        neighbor.current_load += flow
        
        # 3. Process Volatility (Work)
        processed_total = 0
        for agent in self.agent_list:
            # Base Capacity
            cap = 1.0
            if agent.agent_type == 'LLM': cap = 5.0
            elif agent.agent_type == 'Robot': cap = 3.0
            agent.base_capacity = cap # Store for H calculation
            
            # Process
            work = min(agent.current_load, cap)
            agent.current_load -= work
            processed_total += work
            
            # Trust Update (Eq 149: dTau/dt = alpha * Labor - beta * Cost)
            # If successful work, generate Trust
            if work > 0:
                # Strengthen links to neighbors (Reputation spread)
                neighbors = list(self.G.neighbors(agent.unique_id))
                for nid in neighbors:
                    self.G[agent.unique_id][nid]['weight'] = min(1.0, self.G[agent.unique_id][nid]['weight'] + 0.001)
            
            # Decay (Trust Decay)
            # Unused trust decays? Or general decay?
            # Let's decay links slightly
            neighbors = list(self.G.neighbors(agent.unique_id))
            for nid in neighbors:
                self.G[agent.unique_id][nid]['weight'] *= 0.999 # Slow decay

        # Global Volatility is sum of remaining loads
        self.volatility_index = sum(a.current_load for a in self.agent_list)
        self.completed_tasks_count += processed_total
        
        # Calculate Metrics
        self.total_trust = sum([d['weight'] for u, v, d in self.G.edges(data=True)])
        self.current_hamiltonian = self.calculate_hamiltonian()
        
        self.datacollector.collect(self)

    def get_agent(self, unique_id):
        # Helper for list lookup (slow but fine for N=100)
        for a in self.agent_list:
            if a.unique_id == unique_id: return a
        return None

