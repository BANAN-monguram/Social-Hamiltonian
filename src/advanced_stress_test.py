
import numpy as np
import matplotlib.pyplot as plt
import os

def run_advanced_tests():
    print("=== Phase 19: Deep Experimental Defense ===")
    
    if not os.path.exists("stress_results"):
        os.makedirs("stress_results")

    # ==========================================
    # Test A: Trust Latency (The "Meaning" Bottleneck)
    # Critique: Quantum speed is useless if humans don't accept the result.
    # ==========================================
    print("Running Test A: Trust Latency...")
    
    trust_levels = np.linspace(0.1, 1.0, 100) # Trust Score tau
    
    # Time Components
    t_legacy_calc = 100.0 # Old manual calculation
    t_quantum_calc = 0.01 # Deep End calculation (Instant)
    
    # Acceptance Time (Social Friction)
    # T_accept = k / tau^2 (Low trust = Infinite debating time)
    k_friction = 10.0
    
    t_total_legacy = t_legacy_calc + (k_friction / (trust_levels**2))
    t_total_quantum = t_quantum_calc + (k_friction / (trust_levels**2))
    
    plt.figure(figsize=(10, 6))
    
    # Plot Legacy
    # plt.plot(trust_levels, t_total_legacy, label='Legacy System (Manual Calc)', color='gray', linestyle='--')
    
    # Plot Quantum
    plt.plot(trust_levels, t_total_quantum, label='CSCT (Quantum Calc)', color='blue', linewidth=2)
    
    # Threshold for "Practical Solution"
    plt.axhline(20.0, color='red', linestyle=':', label='Social Deadline (Time Limit)')
    
    plt.yscale('log')
    plt.title('The Trust Bottleneck: Why Compute Speed is Not Enough')
    plt.xlabel('Social Trust Level (tau)')
    plt.ylabel('Total Resolution Time (Calc + Acceptance) [Log Scale]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Annotate the "Useless Zone"
    plt.text(0.2, 500, "Compute speed irrelevant here\n(Dominated by Mistrust)", color='red')
    plt.text(0.7, 2, "Quantum Advantage Active", color='green')
    
    plt.savefig('stress_results/thesis_fig_trust_bottleneck.png')
    plt.close()


    # ==========================================
    # Test B: The Auto-Immune Paradox (Optimization vs Entropy)
    # Critique: System optimization kills the very human noise it needs.
    # ==========================================
    print("Running Test B: Auto-Immune Paradox...")
    
    time_steps = 200
    
    # Scenario 1: Totalitarian Optimization (Goal: Order -> 1.0)
    order_1 = 0.5
    value_history_1 = []
    
    # Scenario 2: "Wildness Reservation" (Goal: Order -> 0.7)
    order_2 = 0.5
    value_history_2 = []
    
    for t in range(time_steps):
        # Scenario 1: Aggressive Optimization
        order_1 += 0.005 
        if order_1 > 0.99: order_1 = 0.99
        
        # Scenario 2: Balanced Optimization
        if order_2 < 0.7:
            order_2 += 0.005
        
        # Value Function V = Order * Innovation
        # Innovation I = f(Freedom) = f(1 - Order)
        # Let's model I = 4 * (1-O) * O (inverted U shape? No, usually I increases with Freedom)
        # Simply: I = (1 - Order)^2  (Freedom is raw material for novelty)
        # But wait, total anarchy (Order=0) also has low value (No coordination).
        # V = Order * (1 - Order) * Scale?
        # Critique says "Noise Source" is human.
        # Innovation = (1 - Order) (Chaos power)
        # Coordination = Order
        # Economic Value = Coordination * Innovation
        
        # Scen 1
        innov_1 = (1.0 - order_1) * 2.0
        # If Order -> 1, Innov -> 0.
        val_1 = order_1 * innov_1
        value_history_1.append(val_1)
        
        # Scen 2
        innov_2 = (1.0 - order_2) * 2.0
        val_2 = order_2 * innov_2
        value_history_2.append(val_2)
        
    plt.figure(figsize=(10, 6))
    plt.plot(value_history_1, label='Totalitarian Optimization (Order -> 1.0)', color='red')
    plt.plot(value_history_2, label='Ecological Balance (Order -> 0.7)', color='green', linewidth=2)
    
    plt.axvline(100, color='gray', linestyle='--')
    plt.text(105, 0.4, "Optimization Trap\n(Auto-Immune Collapse)", color='red')
    
    plt.title('The Auto-Immune Paradox: Optimization Kills Value')
    plt.xlabel('Time (Optimization Progress)')
    plt.ylabel('Total Economic Value (Order x Innovation)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('stress_results/thesis_fig_auto_immune.png')
    plt.close()
    
    print("Done.")

if __name__ == "__main__":
    run_advanced_tests()
