from unified_model import UnifiedCSCTModel
import matplotlib.pyplot as plt
import numpy as np
import random

def run_stress_test():
    print("=== Phase 4: Crash Test (Identifying Phase Transition) ===")
    model = UnifiedCSCTModel()
    model.era = "Optimized"
    
    loads = []
    volatilities = []
    trust_levels = []
    
    # Ramp up stress
    max_steps = 100
    base_task_count = 10
    
    print("Injecting Exponential Load...")
    for i in range(max_steps):
        # Stress Factor: Exponential growth
        stress_factor = 1.0 + (i * 0.1) # Grow load
        
        # Real Stress Injection
        model.active_task_count = int(base_task_count * stress_factor)
        
        # Decay trust artificially
        decay_rate = 0.95 # severe decay
        for u, v in model.G.edges:
            model.G[u][v]['weight'] *= decay_rate
            
        model.step()
        
        # Metrics
        v = model.entropy # Serving as proxy for volatility/chaos
        t = model.social_trust
        
        loads.append(i) # Time/Decay steps
        volatilities.append(v)
        trust_levels.append(t)
        
        print(f"Step {i}: Trust={t:.4f}, Entropy={v:.2f}")
        
        if v > 200: # Explosion threshold
            print(f"!!! CRITICAL FAILURE AT STEP {i} !!!")
            print("System collapsed due to Trust Depletion.")
            break

    # Visualization
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.set_xlabel('Stress Steps (Trust Decay)')
    ax1.set_ylabel('Social Entropy (Chaos)', color='red')
    ax1.plot(loads, volatilities, color='red', linewidth=2, label='Entropy (Volatility)')
    ax1.tick_params(axis='y', labelcolor='red')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Network Trust', color='blue')
    ax2.plot(loads, trust_levels, color='blue', linestyle='--', label='Trust Level')
    ax2.tick_params(axis='y', labelcolor='blue')
    
    plt.title('Crash Test: System Stability Limit (Phase Transition)')
    plt.grid(True)
    plt.savefig('phase4_crash_test.png')
    print("Saved phase4_crash_test.png")

if __name__ == "__main__":
    run_stress_test()
