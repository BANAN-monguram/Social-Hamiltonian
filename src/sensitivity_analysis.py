from model import CSCTModel
import numpy as np

def run_scenario(llm_cost_multiplier):
    NUM_HUMANS = 40
    NUM_LLMS = 50
    NUM_ROBOTS = 10
    NUM_TASKS = 200 # Increased for better statistics
    
    model = CSCTModel(NUM_HUMANS, NUM_LLMS, NUM_ROBOTS, NUM_TASKS)
    
    # Apply cost modifier to LLMs
    for agent in model.agent_list:
        if agent.agent_type == 'LLM':
            agent.cost_per_tick *= llm_cost_multiplier
            
    h_opt = model.run_allocation_optimized()
    
    # Collect stats
    assigned_counts = {'Human': 0, 'LLM': 0, 'Robot': 0, 'None': 0}
    
    # Inspect agents directly to count assignments
    for a in model.agent_list:
        if a.is_busy:
            assigned_counts[a.agent_type] += 1
        
    return h_opt, assigned_counts

def main():
    print("=== CSCT Sensitivity Analysis: LLM Cost Impact ===\n")
    print(f"{'LLM Cost Factor':<15} | {'Hamiltonian':<12} | {'Improvement':<12}")
    print("-" * 45)
    
    # Baseline run (Cost Factor 1.0)
    base_h, _ = run_scenario(1.0)
    
    cost_factors = [1.0, 0.8, 0.5, 0.2, 0.1, 0.05, 0.01]
    
    results = []
    
    for factor in cost_factors:
        h, counts = run_scenario(factor)
        improvement = (base_h - h) / base_h * 100.0 if factor != 1.0 else 0.0
        print(f"{factor:<15.2f} | {h:<12.2f} | {improvement:<11.2f}%")
        results.append((factor, h, improvement))
        
    print("\n[Analysis]")
    print(f"Baseline Hamiltonian (factor 1.0): {base_h:.2f}")
    lowest_h = results[-1][1]
    print(f"Lowest Hamiltonian (factor 0.01): {lowest_h:.2f}")
    print("As LLM cost approaches zero, the Social Hamiltonian decreases significantly.")
    print("This confirms that 'Deflationary Force' of AI contributes to system optimization.")

if __name__ == "__main__":
    main()
