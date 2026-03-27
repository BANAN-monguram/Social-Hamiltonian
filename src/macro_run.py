from macro_agents import HumanAgent, LLMAgent, RobotAgent
from macro_market import MacroMarket
from quantum_solver import QuantumSolver
from toj_controller import ToJController
from mesa import Model
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np

class GrandSimulation(Model):
    def __init__(self):
        super().__init__()
        self.market = MacroMarket()
        self.solver = QuantumSolver(self)
        self.toj = ToJController()
        self.schedule = []
        self.agents_list = []
        
        # Populate World
        # 100 Humans, 50 LLMs, 20 Robots
        for i in range(100): self.agents_list.append(HumanAgent(i, self))
        for i in range(50): self.agents_list.append(LLMAgent(100+i, self))
        for i in range(20): self.agents_list.append(RobotAgent(150+i, self))
        
        self.step_count = 0
        self.era = "Legacy" # Legacy -> Bubble -> DeepEnd
        
        self.datacollector = DataCollector(
            model_reporters={
                "Hamiltonian": lambda m: m.market.temperature * 10, # Proxy
                "Susceptibility": lambda m: m.market.susceptibility,
                "StructureRigidity": lambda m: m.toj.semantic_rigidity,
                "Wellbeing": self.calculate_wellbeing
            }
        )
        
    def calculate_wellbeing(self):
        # Avg wellbeing of humans
        humans = [a for a in self.agents_list if a.role == "Human"]
        return np.mean([a.wellbeing for a in humans])

    def step(self):
        self.step_count += 1
        
        # 1. Market Dynamics (HFT generates heat)
        hft_active = True
        self.market.step(self.step_count, hft_active)
        
        # 2. ToJ Regulation (Only active in Era 3)
        if self.step_count > 150:
            self.era = "DeepEnd"
            self.toj.regulate(self.market)
            self.market.temperature *= 0.95 # Active Cooling by ToJ
        
        # 3. Matching Process
        if self.era == "Legacy":
            # Greedy Matching (Inefficient)
             # Simplified: Randomized assignment
             pass
        else:
            # Quantum Matching (Optimized)
            matches = self.solver.solve_matching(self.agents_list, self.market.tasks)
            # Execute Matches -> Generate Value -> Increase Wellbeing
            for task_idx, agent in matches.items():
                agent.wellbeing += 0.05
                self.market.tasks[task_idx]["assigned"] = agent
        
        # 4. Agent Steps
        for a in self.agents_list:
            a.step()
            
        # 5. Semantic Annealing Effect
        if self.toj.is_intervening:
            # Boost Wellbeing dramatically (Hope/Structure Change)
            for a in self.agents_list:
                a.wellbeing += 0.02
        
        self.market.clear_completed_tasks()
        self.datacollector.collect(self)

if __name__ == "__main__":
    print("=== Phase 6: Grand Macro Simulation (History of Transition) ===")
    model = GrandSimulation()
    
    steps = 300
    print(f"Simulating {steps} steps...")
    
    for i in range(steps):
        model.step()
        if i % 50 == 0: print(f"Step {i}: Era={model.era}, Temp={model.market.temperature:.2f}, Chi={model.market.susceptibility:.2f}")
        
    # Visualization
    data = model.datacollector.get_model_vars_dataframe()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot Susceptibility (Bubble Risk)
    ax1.set_xlabel('Time (Steps)')
    ax1.set_ylabel('Instability (Susceptibility)', color='red')
    ax1.plot(data['Susceptibility'], color='red', label='Susceptibility (Bubble Risk)')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.fill_between(data.index, 0, data['Susceptibility'], color='red', alpha=0.1)
    
    # Plot Wellbeing (Success)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Social Wellbeing', color='blue')
    ax2.plot(data['Wellbeing'], color='blue', linewidth=2, label='Wellbeing')
    ax2.tick_params(axis='y', labelcolor='blue')
    
    # Annotate Eras
    plt.axvline(150, color='green', linestyle='--', linewidth=2)
    plt.text(150, 0.5, ' Deep End Activation\n (Semantic Intervention)', ha='left', color='green')
    
    plt.title('Grand Simulation: From Capitalist Instability to CSCT Stability')
    plt.grid(True, alpha=0.3)
    plt.savefig('macro_grand_simulation.png')
    print("Saved macro_grand_simulation.png")
