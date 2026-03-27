import numpy as np
import matplotlib.pyplot as plt
from mesa import Model, Agent
from mesa.datacollection import DataCollector
import random

class SemanticAgent(Agent):
    def __init__(self, unique_id, model, vector_dim=5):
        super().__init__(model) # Mesa 3.x
        self.unique_id = unique_id
        # Internal "Values" (Vector representation of what they care about)
        self.value_vector = np.random.normal(0, 1, vector_dim)
        self.value_vector /= np.linalg.norm(self.value_vector) # Normalize
        
        self.satisfaction = 0.0

    def step(self):
        # Satisfaction depends on alignment with the "Global Narrative"
        narrative = self.model.current_narrative
        if narrative is not None:
            # Cosine similarity
            resonance = np.dot(self.value_vector, narrative)
            self.satisfaction = resonance # Can be negative (Dissonance)

class GovernanceAI(Agent):
    """The 'Deep End' LLM that generates narratives."""
    def __init__(self, unique_id, model):
        super().__init__(model)
        
    def step(self):
        # Look for a narrative that maximizes total satisfaction (Gradient Descent-ish)
        # For simulation, we randomly sample "Concepts" and keep the best one (Evolutionary Strategy)
        best_narrative = self.model.current_narrative
        best_score = self.model.total_satisfaction
        
        # Try a mutation of the narrative (New slogan/idea)
        candidate = self.model.current_narrative + np.random.normal(0, 0.2, 5)
        candidate /= np.linalg.norm(candidate)
        
        # Evaluate "Virtual Score" (Internal simulation)
        score = 0
        for a in self.model.agents_layer:
            score += np.dot(a.value_vector, candidate)
            
        if score > best_score:
            self.model.current_narrative = candidate # Deploy new narrative

class SemanticModel(Model):
    """
    Phase 3: Semantic Intervention.
    Simulates how a 'Narrative' (Vector) unifies scattered agents.
    """
    def __init__(self, num_agents=50):
        super().__init__()
        self.current_narrative = np.random.normal(0, 1, 5)
        self.current_narrative /= np.linalg.norm(self.current_narrative)
        
        self.agents_layer = []
        self.gov_agent = GovernanceAI(999, self)
        
        for i in range(num_agents):
            a = SemanticAgent(i, self)
            self.agents_layer.append(a)
            
        self.datacollector = DataCollector(
            model_reporters={
                "TotalSatisfaction": lambda m: m.total_satisfaction,
                "NarrativeCoherence": lambda m: np.linalg.norm(m.current_narrative)
            }
        )
        self.total_satisfaction = 0

    def step(self):
        self.gov_agent.step() # AI proposes new narrative
        
        self.total_satisfaction = 0
        for a in self.agents_layer:
            a.step()
            self.total_satisfaction += a.satisfaction
            
        self.datacollector.collect(self)

if __name__ == "__main__":
    # Quick Test
    model = SemanticModel()
    print("Initial Satisfaction:", model.total_satisfaction)
    for i in range(50):
        model.step()
    print("Final Satisfaction (After AI Intervention):", model.total_satisfaction)
