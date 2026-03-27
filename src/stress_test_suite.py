
import numpy as np
import matplotlib.pyplot as plt
import os

def run_stress_tests():
    print("=== Phase 17: Experimental Stress Tests (Reality Check) ===")
    
    if not os.path.exists("stress_results"):
        os.makedirs("stress_results")

    # ==========================================
    # Test 1: Cascade Failure (Physical Fragility)
    # ==========================================
    # Critique: Parameters are not independent. Disaster damages Infra, which kills recovery.
    print("Running Test 1: Cascade Failure...")
    
    years = 200
    capital = 100.0
    infra_health = 1.0 # 0.0 - 1.0
    output_history = []
    infra_history = []
    
    # 3 High-frequency disasters to trigger cascade
    disaster_schedule = [50, 52, 54] 
    
    for y in range(years):
        shock = 0.0
        if y in disaster_schedule:
            shock = 0.3 # 30% direct damage
            
        # 1. Direct Damage
        capital *= (1.0 - shock)
        infra_health *= (1.0 - shock * 1.5) # Infra is more fragile than capital
        
        # 2. Production (Dependent on Infra!)
        # Non-linear penalty: If Infra < 0.5, Output crashes
        productivity = 1.0 * (infra_health ** 2) 
        output = productivity * (capital ** 0.4)
        output_history.append(output)
        infra_history.append(infra_health)
        
        # 3. Recovery (Dependent on Capital!)
        # If Capital is low, we can't fix Infra
        recovery_capacity = 0.02 * (capital / 100.0)
        infra_health += recovery_capacity
        if infra_health > 1.0: infra_health = 1.0
        
        # Reinvestment
        capital += output * 0.2
        capital *= 0.95 # Depreciation
        
    plt.figure(figsize=(10, 6))
    plt.plot(output_history, label='Economic Output', color='blue')
    plt.plot(infra_history, label='Infrastructure Health', color='red', linestyle='--')
    plt.axvline(50, color='black', alpha=0.3, label='Disaster Cluster')
    plt.title('Stress Test 1: Cascade Failure (Infra Collapse)')
    plt.xlabel('Year')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('stress_results/thesis_fig_cascade_failure.png')
    plt.close()

    # ==========================================
    # Test 2: Political Friction (Resistance Energy)
    # ==========================================
    # Critique: Rapid reform causes political backlash (Resistance).
    print("Running Test 2: Political Friction...")
    
    years = 100
    param_value = 0.0 # e.g., Tax Rate
    target_value = 1.0
    
    hist_naive = []
    hist_aware = []
    
    # Agents
    p_naive = 0.0
    p_aware = 0.0
    resistance = 0.0
    
    for y in range(years):
        # Naive: Fast Optimization (Speed = 0.1)
        # Friction = speed^2. If Friction > 0.005, Rollback occurs (Backlash)
        naive_speed = 0.1
        friction = naive_speed ** 2
        
        # Naive Controller ignores friction
        p_naive += naive_speed 
        
        # BUT: The "Society" rejects it if too fast
        if friction > 0.005: 
            p_naive -= naive_speed * 1.5 # Rollback + Punishment
            
        hist_naive.append(p_naive)
        
        # Aware: Slow Optimization (Adiabatic)
        # Speed = 0.05
        aware_speed = 0.05
        friction_aware = aware_speed ** 2
        
        if friction_aware <= 0.005:
            p_aware += aware_speed
        else:
             p_aware -= aware_speed # Should not happen
             
        hist_aware.append(p_aware)

    plt.figure(figsize=(10, 6))
    plt.plot(hist_naive, label='Naive Optimization (Fast)', color='red', linestyle='--')
    plt.plot(hist_aware, label='Adiabatic Optimization (Slow/Aware)', color='green')
    plt.title('Stress Test 2: Political Friction & Backlash')
    plt.xlabel('Time (Step)')
    plt.ylabel('Optimization Progress')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('stress_results/thesis_fig_friction_resistance.png')
    plt.close()

    # ==========================================
    # Test 3: The Entropy Paradox (Self-Defeating Optimization)
    # ==========================================
    # Critique: If Humans become "Optimal" (Rational), they lose "Entropy Value".
    print("Running Test 3: Entropy Paradox...")
    
    years = 200
    human_rationality = 0.0 # Starts irrational
    system_efficiency = 1.0
    
    hist_eff = []
    hist_rat = []
    
    for y in range(years):
        # System optimizes Humans (Education/Nudge)
        human_rationality += 0.01 
        if human_rationality > 1.0: human_rationality = 1.0
        
        # Efficiency = Base + Rationality Bonus
        # BUT: If Rationality > 0.8, "Novelty" drops -> Innovation Stalls
        
        novelty_factor = 1.0
        if human_rationality > 0.8:
            # Over-optimized: Novelty crashes
            over_opt = (human_rationality - 0.8) * 5.0 # 0.0 to 1.0
            novelty_factor = 1.0 - over_opt # Crashes to 0
            
        # Total System Efficiency
        # Efficiency gains from rationality vs Innovation loss from no novelty
        curr_eff = (1.0 + human_rationality * 0.5) * novelty_factor
        
        hist_eff.append(curr_eff)
        hist_rat.append(human_rationality)

    plt.figure(figsize=(10, 6))
    plt.plot(hist_eff, label='System Efficiency', color='purple')
    plt.plot(hist_rat, label='Human Rationality', color='gray', linestyle=':')
    plt.axvline(80, color='red', linestyle='--', label='Novelty Collapse Point')
    plt.title('Stress Test 3: The Entropy Paradox (Over-Optimization)')
    plt.xlabel('Year (Optimization Level)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('stress_results/thesis_fig_human_homogenization.png')
    plt.close()
    
    print("All stress tests completed.")

if __name__ == "__main__":
    run_stress_tests()
