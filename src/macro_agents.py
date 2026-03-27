from mesa import Agent
import numpy as np

class MacroAgent(Agent):
    def __init__(self, unique_id, model, role, dim=5):
        super().__init__(model)
        self.unique_id = unique_id
        self.role = role # "Human", "LLM", "Robot"
        self.dim = dim
        self.pos = np.random.normal(0, 1, dim) # Position in Skill Space
        self.wealth = 0.0
        self.wellbeing = 0.5
        self.current_task = None
        
    def step(self):
        # Basic metabolism (Cost of Living)
        self.wealth -= 0.01 
        if self.wealth < 0: self.wealth = 0

class HumanAgent(MacroAgent):
    def __init__(self, unique_id, model, dim=5):
        super().__init__(unique_id, model, "Human", dim)
        self.innovation_rate = 0.1 # Ability to create new Tasks
        
    def step(self):
        super().step()
        # Humans wander (Innovation/Entropy)
        self.pos += np.random.normal(0, 0.1, self.dim)

class LLMAgent(MacroAgent):
    def __init__(self, unique_id, model, dim=5):
        super().__init__(unique_id, model, "LLM", dim)
        self.error_rate = 0.05 # Hallucination
        self.compute_speed = 10.0
        
    def step(self):
        super().step()
        # LLMs are static unless retrained (moved by ToJ)
        pass 

class RobotAgent(MacroAgent):
    def __init__(self, unique_id, model, dim=5):
        super().__init__(unique_id, model, "Robot", dim)
        self.energy_cost = 0.5
        
    def step(self):
        super().step()
        self.wealth -= self.energy_cost # High maintenance
