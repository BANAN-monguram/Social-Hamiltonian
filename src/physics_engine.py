import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.datacollection import DataCollector

class ParticleAgent(Agent):
    """
    An agent represented as a particle in D-dimensional skill space.
    """
    def __init__(self, unique_id, model, dim=2):
        super().__init__(model)
        self.unique_id = unique_id
        # State Vector sigma (Position in Skill Space)
        self.pos = np.random.normal(0, 5, dim) 
        self.velocity = np.zeros(dim)
        
    def step(self):
        # Langevin Dynamics: dx = (-grad H) * dt + sigma * dW
        dt = self.model.dt
        
        # 1. Deterministic Force (Gradient of Hamiltonian)
        # H = Sum (pos - task_pos)^2 (Harmonic Potential)
        force = np.zeros_like(self.pos)
        
        # Pull towards optimal task match
        if self.model.current_task is not None:
             # F = -k * (x - x0)
            k = self.model.coupling_strength # "J" parameter
            dist = self.pos - self.model.current_task
            force -= k * dist
            
        # 2. Stochastic Force (Thermal Noise / Market Volatility)
        noise = np.random.normal(0, np.sqrt(self.model.temperature * dt), size=self.pos.shape)
        
        # Update Position (Euler-Maruyama)
        self.pos += force * dt + noise
        
        # Boundary condition (Soft containment)
        if np.linalg.norm(self.pos) > 100:
            self.pos *= 0.99

class PhysicsModel(Model):
    """
    Simulates Society as a Thermodynamic System.
    """
    def __init__(self, num_agents=50, temperature=1.0, coupling=1.0):
        super().__init__()
        self.num_agents = num_agents
        self.temperature = temperature # T (Noise)
        self.coupling_strength = coupling # J (Optimization Power)
        self.dt = 0.1
        self.dim = 2
        
        self.schedule = [] # Manual scheduling for simple loop
        self.agents_list = []
        
        # Create Agents
        for i in range(num_agents):
            a = ParticleAgent(i, self, self.dim)
            self.agents_list.append(a)
            
        # Task Attractor (The "Ideal" State)
        self.current_task = np.zeros(self.dim) # Center
        
        self.datacollector = DataCollector(
            model_reporters={
                "Hamiltonian": self.calculate_hamiltonian,
                "OrderParam": self.calculate_order_param
            }
        )

    def calculate_hamiltonian(self):
        # H = Sum (x - x_task)^2
        total_energy = 0
        for a in self.agents_list:
            total_energy += np.linalg.norm(a.pos - self.current_task)**2
        return total_energy / self.num_agents

    def calculate_order_param(self):
        # 1 / Mean Distance (High when clustered/optimized)
        mean_dist = np.mean([np.linalg.norm(a.pos - self.current_task) for a in self.agents_list])
        return 1.0 / (mean_dist + 1e-6)

    def step(self):
        for a in self.agents_list:
            a.step()
        self.datacollector.collect(self)

if __name__ == "__main__":
    # Relaxation Test
    print("Testing Relaxation Dynamics...")
    model = PhysicsModel(temperature=1.0, coupling=0.5)
    
    # Run
    for _ in range(100):
        model.step()
        
    print("Final Energy:", model.calculate_hamiltonian())
