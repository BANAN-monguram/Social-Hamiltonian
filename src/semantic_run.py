from semantic_model import SemanticModel
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def run_semantic_simulation():
    print("=== Phase 3: Semantic Intervention (Deep End Narrative) ===")
    
    # 1. Run Model
    model = SemanticModel(num_agents=100)
    steps = 100
    
    # Force initial dissatisfaction to simulate "Crisis"
    # Set narrative opposite to population mean
    pop_mean = np.mean([a.value_vector for a in model.agents_layer], axis=0)
    model.current_narrative = -pop_mean # Maximum Dissonance
    
    print("Simulating Narrative Optimization...")
    for _ in range(steps):
        model.step()
        
    data = model.datacollector.get_model_vars_dataframe()
    
    # 2. Visualize
    plt.figure(figsize=(10, 6))
    plt.plot(data['TotalSatisfaction'], color='purple', linewidth=2)
    plt.title('Impact of Semantic Intervention on Social Cohesion')
    plt.xlabel('Time Step (Narrative Iterations)')
    plt.ylabel('Total Satisfaction (Alignment)')
    plt.axhline(0, color='gray', linestyle='--')
    plt.grid(True, alpha=0.3)
    
    # Annotate
    start_val = data['TotalSatisfaction'].iloc[0]
    end_val = data['TotalSatisfaction'].iloc[-1]
    plt.text(5, start_val, 'Initial Crisis\n(Narrative Mismatch)', color='red')
    plt.text(80, end_val, 'Convergence\n(Unified Meaning)', color='purple', ha='center', va='bottom')
    
    plt.savefig('phase3_semantic_result.png')
    print("Saved phase3_semantic_result.png")
    
    print(f"Satisfaction Improved: {start_val:.2f} -> {end_val:.2f}")

if __name__ == "__main__":
    run_semantic_simulation()
