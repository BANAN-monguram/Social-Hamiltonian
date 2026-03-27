from mesa import Agent
import numpy as np

class TensorAgent(Agent):
    """
    Base Agent defined by Generalized Labor Tensor (Ch3).
    State w = (E, I, S)
    """
    def __init__(self, unique_id, model, agent_type, E, I, S, error_rate=0.0, risk_factor=1.0):
        super().__init__(model) # Mesa 3.x simplified init
        self.unique_id = unique_id
        self.agent_type = agent_type
        
        # The Tensor (Capabilities/Properties)
        self.E = E # Energy consumption (Cost)
        self.I = I # Information processing capacity
        self.S = S # Entropy capacity (Creativity/Novelty)
        
        # Risk Profile (Critique #1)
        self.error_rate = error_rate # Probability of failure/hallucination
        self.risk_factor = risk_factor # Magnitude of damage if failure occurs
        
        # Dynamic State
        self.trust = 0.5 # Tau (0.0 - 1.0)
        self.well_being = 0.5 # W (0.0 - 1.0)
        self.is_busy = False
        self.wealth = 0.0 # Earned tokens
        
    def step(self):
        # Natural Trust Decay (Ch5)
        self.trust *= 0.99 
        
        # Cost of living (Entropy increase)
        self.wealth -= self.E * 0.01

class HumanAgent(TensorAgent):
    """
    Human: High Cost, Low I, High S. Reliable (Low Error).
    """
    def __init__(self, unique_id, model):
        # E=10.0 (High), I=1.0 (Base), S=10.0 (High Creativity)
        # Error: 1% (Human Error), Risk: Low (Common sense checks)
        super().__init__(unique_id, model, "Human", E=10.0, I=1.0, S=10.0, error_rate=0.01, risk_factor=1.0)

class LLMAgent(TensorAgent):
    """
    LLM: Low Cost, Ultra-High I, Low S. Prone to Hallucination (Critique #1).
    """
    def __init__(self, unique_id, model):
        # E=0.1 (Low), I=100.0 (High), S=1.0 (Low Creativity)
        # Error: 5% (Hallucination), Risk: High (Scale propagation)
        super().__init__(unique_id, model, "LLM", E=0.1, I=100.0, S=1.0, error_rate=0.05, risk_factor=50.0)

class RobotAgent(TensorAgent):
    """
    Robot: Med Cost, High I, Zero S. Reliable.
    """
    def __init__(self, unique_id, model):
        # E=2.0 (Energy), I=50.0, S=0.0 (Deterministic)
        # Error: Very Low, Risk: Medium (Physical damage)
        super().__init__(unique_id, model, "Robot", E=2.0, I=50.0, S=0.0, error_rate=0.001, risk_factor=5.0)
