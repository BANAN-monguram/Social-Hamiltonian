import numpy as np
from model import CSCTModel
from agents import HumanAgent, LLMAgent, RobotAgent
import sys

def run_monte_carlo(iterations=100):
    print(f"=== CSCT Robustness Verification (Monte Carlo: {iterations} Runs) ===")
    print("Randomizing: Agent Costs, Task Distribution, Capability Means")
    print("-" * 60)
    
    results = []
    wins = 0
    
    for i in range(iterations):
        # 1. Randomize Environment Parameters
        # Costs
        llm_cost_mean = np.random.uniform(0.01, 5.0) # LLM can be expensive?
        human_cost_mean = np.random.uniform(5.0, 20.0)
        
        # Task Distribution
        # Random weights summing to 1.0
        weights = np.random.dirichlet(np.ones(3), size=1)[0]
        # weights = [p_logic, p_creative, p_physical]
        
        # 2. Initialize Model
        # Note: We re-generate tasks manually after init to apply new weights
        model = CSCTModel(num_humans=40, num_llms=50, num_robots=10, task_count=200)
        
        # 3. Apply Randomized Parameters to Agents
        for agent in model.agent_list:
            if agent.agent_type == 'LLM':
                agent.cost_per_tick = llm_cost_mean
            elif agent.agent_type == 'Human':
                agent.cost_per_tick = human_cost_mean
                
        # 4. Regenerate Tasks with new distribution
        model.tasks = []
        task_types = ['Logic', 'Creative', 'Physical']
        for tid in range(200):
            t_type = np.random.choice(task_types, p=weights)
            diff = np.random.random()
            model.tasks.append({
                'id': tid,
                'type': t_type,
                'difficulty': diff,
                'assigned_to': None
            })
            
        # 5. Run Comparison
        h_greedy = model.run_allocation_greedy()
        h_opt = model.run_allocation_optimized()
        
        improvement = (h_greedy - h_opt) / h_greedy * 100.0 if h_greedy != 0 else 0.0
        
        results.append({
            'run': i,
            'improvement': improvement,
            'llm_cost': llm_cost_mean,
            'human_cost': human_cost_mean,
            'task_dist': weights
        })
        
        if h_opt < h_greedy:
            wins += 1
            
        if i % 10 == 0:
            print(f"Run {i}: Improvement {improvement:.2f}% (LLM Cost: {llm_cost_mean:.2f})")

    # Statistics
    improvements = [r['improvement'] for r in results]
    mean_imp = np.mean(improvements)
    std_imp = np.std(improvements)
    min_imp = np.min(improvements)
    max_imp = np.max(improvements)
    
    print("-" * 60)
    print(f"Total Runs: {iterations}")
    print(f"Optimization Win Rate: {wins}/{iterations} ({wins/iterations*100:.1f}%)")
    print(f"Mean Improvement: {mean_imp:.2f}%")
    print(f"Std Dev: {std_imp:.2f}%")
    print(f"Min Improvement: {min_imp:.2f}%")
    print(f"Max Improvement: {max_imp:.2f}%")
    
    print("\n[Conclusion]")
    if mean_imp > 10.0 and wins/iterations > 0.9:
        print("PASS: The algorithm is robustly effective across randomized environments.")
    else:
        print("FAIL: The algorithm performance is unstable or insignificant.")

if __name__ == "__main__":
    run_monte_carlo()
