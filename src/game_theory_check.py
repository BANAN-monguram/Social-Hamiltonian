import numpy as np
import matplotlib.pyplot as plt
from mesa import Model, Agent
from mesa.datacollection import DataCollector
import random

class GameAgent(Agent):
    def __init__(self, unique_id, model, strategy="Honest"):
        super().__init__(model)
        self.unique_id = unique_id
        self.strategy = strategy # "Honest" or "Cheat"
        self.utility = 0
        
    def step(self):
        # Payoffs
        REWARD = 10.0
        COST_HONEST = 5.0
        COST_CHEAT = 0.5
        PENALTY = 50.0 # Slashing
        
        # Audit Probability (Deep End Verification)
        # In a real system, this comes from ZK-Proof verification cost trade-offs
        PROB_AUDIT = 0.15 
        
        if self.strategy == "Honest":
            self.utility = REWARD - COST_HONEST
        else: # Cheat
            # Cheating is gambling
            if random.random() < PROB_AUDIT:
                # Caught!
                self.utility = REWARD - COST_CHEAT - PENALTY
            else:
                # Got away with it
                self.utility = REWARD - COST_CHEAT

class GameModel(Model):
    """
    Evolutionary Game Model.
    """
    def __init__(self, num_agents=1000):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = [] 
        self.agents_list = []
        
        # Init 50/50 split
        for i in range(num_agents):
            strat = "Honest" if i < num_agents/2 else "Cheat"
            a = GameAgent(i, self, strat)
            self.agents_list.append(a)
            
        self.datacollector = DataCollector(
            model_reporters={
                "CheatRatio": lambda m: sum(1 for a in m.agents_list if a.strategy=="Cheat") / m.num_agents,
                "AvgUtility": lambda m: np.mean([a.utility for a in m.agents_list])
            }
        )

    def step(self):
        # 1. Play Game
        for a in self.agents_list:
            a.step()
            
        # 2. Replicator Dynamics (Evolution)
        # Calculate avg utility per strategy
        honest_agents = [a for a in self.agents_list if a.strategy == "Honest"]
        cheat_agents = [a for a in self.agents_list if a.strategy == "Cheat"]
        
        u_honest = np.mean([a.utility for a in honest_agents]) if honest_agents else 0
        u_cheat = np.mean([a.utility for a in cheat_agents]) if cheat_agents else 0
        
        # Agents switch strategies based on success
        # Simple rule: X% of agents switch to better strategy
        switch_rate = 0.05
        
        better_strat = "Honest" if u_honest > u_cheat else "Cheat"
        
        # If Honest is better, Cheaters switch to Honest
        if u_honest > u_cheat:
            for a in cheat_agents:
                if random.random() < switch_rate:
                    a.strategy = "Honest"
        elif u_cheat > u_honest:
             for a in honest_agents:
                if random.random() < switch_rate:
                    a.strategy = "Cheat"

        self.datacollector.collect(self)

if __name__ == "__main__":
    print("=== Physics Experiment 3: Game Theory (Nash Equilibrium) ===")
    model = GameModel(num_agents=5000)
    
    steps = 500 # Sufficient for 5000 agents
    for i in range(steps):
        model.step()
        
    data = model.datacollector.get_model_vars_dataframe()
    
    plt.figure(figsize=(10, 6))
    plt.plot(data['CheatRatio'], color='red', linewidth=2, label='Ratio of Cheaters')
    
    plt.title('Evolutionary Stability: Extinction of Defectors')
    plt.xlabel('Generations (Time)')
    plt.ylabel('Population Fraction')
    plt.ylim(0, 1.0)
    plt.axhline(0, color='black', linestyle='--')
    plt.text(50, 0.1, 'Convergence to\nHonest Strategy (ESS)', ha='center')
    
    plt.grid(True)
    plt.legend()
    plt.savefig('physics_game_theory.png')
    print("Saved physics_game_theory.png")
    
    final_ratio = data['CheatRatio'].iloc[-1]
    print(f"Final Cheater Ratio: {final_ratio:.4f}")
