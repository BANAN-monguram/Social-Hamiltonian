from mesa import Model
from mesa.datacollection import DataCollector
from unified_agents import HumanAgent, LLMAgent, RobotAgent
import networkx as nx
import numpy as np
import random

class UnifiedCSCTModel(Model):
    """
    The Grand Simulation Model.
    Covers Chapters 3, 4, 5, 6.
    """
    def __init__(self, num_humans=30, num_llms=20, num_robots=10):
        super().__init__()
        self.agent_list = []
        self.G = nx.Graph()
        self.era = "Legacy" # Legacy -> Transition -> Optimized
        
        # Init Agents
        agent_id = 0
        for _ in range(num_humans):
            a = HumanAgent(agent_id, self)
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="Human")
            agent_id += 1
        for _ in range(num_llms):
            a = LLMAgent(agent_id, self)
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="LLM")
            agent_id += 1
        for _ in range(num_robots):
            a = RobotAgent(agent_id, self)
            self.agent_list.append(a)
            self.G.add_node(agent_id, type="Robot")
            agent_id += 1
            
        # Init Trust Network (Ch5)
        self._build_network()
        
        # System Metrics
        self.entropy = 100.0 # S(t) - Starts high (Chaos)
        self.social_trust = 0.0 # Total Tau
        self.volatility = 0.0 # V
        self.hamiltonian = 0.0 # H
        self.dispute_backlog = 0 # Ch4 Legal friction
        self.active_task_count = 10 # Default load
        
        self.datacollector = DataCollector(
            model_reporters={
                "Entropy": "entropy",
                "Trust": "social_trust",
                "Hamiltonian": "hamiltonian",
                "Disputes": "dispute_backlog",
                "Wellbeing": lambda m: sum(a.well_being for a in m.agent_list)
            }
        )

    def _build_network(self):
        # Scale-free for Humans
        for a in self.agent_list:
            if a.agent_type == 'Human':
                # Link to random others
                target = random.choice(self.agent_list)
                if target != a:
                    self.G.add_edge(a.unique_id, target.unique_id, weight=0.1)

    def step(self):
        # Define current logic based on Era
        if self.era == "Legacy":
            self._step_legacy()
        elif self.era == "Transition":
            self._step_transition()
        elif self.era == "Optimized":
            self._step_optimized()
            
        # Record Data
        self.datacollector.collect(self)
        
        # Time evolution
        self.social_trust = sum([self.G[u][v]['weight'] for u, v in self.G.edges]) / (len(self.G.edges) + 1)
        for a in self.agent_list: a.step()

    # --- Era Logic ---

    def _step_legacy(self):
        """
        Era 1: Market Equilibrium (Critique #3: Stronger Baseline).
        Agents rationally choose tasks that minimize their OWN mismatch, but ignore externalities (Social Cost).
        """
        tasks = self._generate_tasks(10)
        current_H = 0
        
        # Nash-like matching: Each task goes to the agent who 'bids' best (locally), 
        # but without global coordination, inefficiencies accumulate.
        for t in tasks:
            # Random sample of 'available' agents bidding
            bidders = random.sample(self.agent_list, k=5)
            # Rational Choice: Bidder with best E/I match wins
            winner = min(bidders, key=lambda a: abs(t['E']-a.E) + abs(t['I']-a.I))
            
            # Outcome
            mismatch = abs(t['E']-winner.E) + abs(t['I']-winner.I)
            current_H += mismatch
            
            # Errors still happen (Individual rationality doesn't prevent accidents)
            if random.random() < winner.error_rate:
                current_H += winner.risk_factor # Panic/Crash
            
            # Dispute Logic
            if mismatch > 10.0 or random.random() < 0.05:
                # Friction is inevitable in Atomized society
                self.dispute_backlog += 1

        # Disputes resolve slowly (Bureaucracy)
        self.dispute_backlog = max(0.1, self.dispute_backlog - 0.2) # Never exactly 0 (Critique #4)
            
        self.hamiltonian = current_H + random.uniform(0, 10) # Add noise
        self.entropy += 1.0 

    def _step_transition(self):
        """
        Era 2: Deep End (Risk-Aware Optimization).
        """
        # Dynamic Task Count for Stress Testing
        tasks = self._generate_tasks(self.active_task_count)
        current_H = 0
        
        for t in tasks:
            best_agent = None
            min_score = float('inf')
            
            # Global Optimization interacting with Vector Space
            for a in self.agent_list:
                # Dist = Tensor Difference
                dist = abs(t['E']-a.E) + abs(t['I']-a.I) + abs(t['S']-a.S)
                
                # RISK MANAGEMENT (Critique #1):
                # The algo checks Trust. Low trust agents are penalized for High Impact tasks.
                risk_penalty = a.error_rate * a.risk_factor * 10.0 * (1.0 - a.trust)
                
                score = dist + risk_penalty # Risk-Adjusted Cost
                
                if score < min_score:
                    min_score = score
                    best_agent = a
            
            # Execute
            if best_agent:
                # 1. Physics Outcome
                real_mismatch = abs(t['E']-best_agent.E) + abs(t['I']-best_agent.I) + abs(t['S']-best_agent.S)
                current_H += real_mismatch
                
                # 2. Probability of Failure
                if random.random() < best_agent.error_rate:
                    # HALLUCINATION OCCURS!
                    # However, Trust Network dampens the blow (Critique #1)
                    # High Trust neighbors absorb the shock
                    avg_neighbor_trust = 0.5
                    neighbors = list(self.G.neighbors(best_agent.unique_id))
                    if neighbors:
                        avg_neighbor_trust = np.mean([self.G[best_agent.unique_id][n]['weight'] for n in neighbors])
                    
                    # Damage = Risk * (1 - TrustCoverage)
                    damage = best_agent.risk_factor * (1.0 - avg_neighbor_trust)
                    current_H += damage
                    
                    # Trust damaged
                    best_agent.trust *= 0.8
                else:
                    # Success -> Trust Build
                    best_agent.trust += 0.01
                    neighbors = list(self.G.neighbors(best_agent.unique_id))
                    for n in neighbors:
                        self.G[best_agent.unique_id][n]['weight'] = min(1.0, self.G[best_agent.unique_id][n]['weight'] + 0.001)

        # Algorithmic Courts
        # Not perfect 0, but negligible (Critique #4)
        if self.dispute_backlog > 0:
            self.dispute_backlog *= 0.1 
            
        self.hamiltonian = current_H + random.uniform(0, 5)
        
        # CRITICAL FIX (Critique #2: Over-damping)
        # Entropy Reduction is NOT guaranteed. It depends on Social Trust.
        # Delta S = Input (Errors/Mismatch) - Output (Trust Processing)
        entropy_inflow = (current_H / 100.0) # Cost generates Chaos
        entropy_outflow = self.social_trust * 5.0 # Trust absorbs Chaos
        
        self.entropy += (entropy_inflow - entropy_outflow)
        
        # Lower bound (Background radiation)
        if self.entropy < 1.0: self.entropy = 1.0

    def _step_optimized(self):
        """Ch6 World: ToJ Macro Control."""
        # Run Transition Logic first
        self._step_transition()
        
        # ToJ Intervention (Ch6)
        # Monitor Entropy/Volatility
        if self.entropy > 50.0:
            # Inject Liquidity (Create Tasks for idle agents)
            # This is "Investment Socialization"
            # It artificially lowers local entropy by engaging agents
            self.entropy -= 5.0 
            
            # Boost Wellbeing (UBC / Rewards)
            for a in self.agent_list:
                a.well_being += 0.01

    def _generate_tasks(self, count):
        tasks = []
        for _ in range(count):
            # Task Vector
            tasks.append({
                'E': random.uniform(0, 10),
                'I': random.uniform(0, 100),
                'S': random.uniform(0, 10)
            })
        return tasks
