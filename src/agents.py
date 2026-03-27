from mesa import Agent
import numpy as np

class CSCTAgent(Agent):
    """Base Agent class for CSCT simulation."""
    def __init__(self, unique_id, model, agent_type):
        super().__init__(model)
        self.unique_id = unique_id
        self.agent_type = agent_type
        self.is_busy = False
        self.current_task = None
        
        # Capabilities (0.0 - 1.0)
        self.creativity = 0.5
        self.logic = 0.5
        self.physical = 0.0
        
        # Economic Properties
        self.cost_per_tick = 0.0
        self.well_being = 0.0
        self.stress = 0.0
        
    def step(self):
        pass

class HumanAgent(CSCTAgent):
    """
    Human Agent:
    - High Creativity
    - High Cost (Living cost)
    - High Well-being impact (Needs meaningful work)
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, "Human")
        self.creativity = np.random.normal(0.8, 0.1)
        self.logic = np.random.normal(0.6, 0.1)
        self.physical = np.random.normal(0.5, 0.2)
        
        self.cost_per_tick = 10.0
        self.well_being = 5.0 # Initial happiness
        
    def step(self):
        # Stress accumulation if overworked or doing mismatched tasks
        if self.is_busy:
            self.stress += 0.1
            # If doing creative work, stress reduces (Flow state)
            if self.current_task and self.current_task['type'] == 'Creative':
                self.stress -= 0.2
                self.well_being += 0.5
        else:
            # Boredom or Anxiety if unemployed (UBC covers survival but not self-actualization)
            self.well_being -= 0.1

class LLMAgent(CSCTAgent):
    """
    LLM Agent:
    - Medium-High Creativity (Stochastic)
    - Very Low Cost
    - No Well-being (Tool)
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, "LLM")
        self.creativity = np.random.normal(0.6, 0.2)
        self.logic = 0.9
        self.physical = 0.0
        
        self.cost_per_tick = 0.1 # Token cost
    
    def step(self):
        pass

class RobotAgent(CSCTAgent):
    """
    Robot Agent:
    - Low Creativity
    - Medium Cost (Energy/Maintenance)
    - High Logic/Physical
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, "Robot")
        self.creativity = 0.0
        self.logic = 0.95
        self.physical = 0.95
        
        self.cost_per_tick = 2.0
    
    def step(self):
        pass
