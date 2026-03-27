import numpy as np

class MacroMarket:
    def __init__(self, dim=5):
        self.dim = dim
        self.tasks = [] # List of vectors
        self.temperature = 1.0 # Market Volatility
        self.transaction_volume = 0 # f
        self.susceptibility = 0.0 # chi
        self.gdp = 0.0
        
    def step(self, step_count, hft_active=True):
        # 1. Task Generation (Human Needs)
        # Randomly spawn new tasks
        if np.random.random() < 0.2:
            new_task = np.random.normal(0, 2, self.dim)
            self.tasks.append({"vec": new_task, "value": 1.0, "assigned": None})
            
        # 2. HFT Dynamics (Bubble Logic)
        if hft_active:
             # HFT increases volume and heat
            self.transaction_volume += 1
            if step_count < 100: # Growth Phase
                self.temperature += 0.05
            elif step_count < 150: # Overheating
                self.temperature += 0.2
        
        # 3. Bubble Risk (Susceptibility)
        # Critical Temp Tc approx 5.0
        T_c = 5.0
        if abs(self.temperature - T_c) < 0.1:
            self.susceptibility = 100.0 # Singularity
        else:
            self.susceptibility = 1.0 / abs(self.temperature - T_c)
            
        # Cap
        if self.susceptibility > 50: self.susceptibility = 50.0
        
    def clear_completed_tasks(self):
        self.tasks = [t for t in self.tasks if t["assigned"] is None]
        
    def get_avg_mismatch(self):
        # Calculate market inefficiency
        # Mock calculation
        return self.temperature * 10.0
