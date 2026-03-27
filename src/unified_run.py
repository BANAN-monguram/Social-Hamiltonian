from unified_model import UnifiedCSCTModel
import matplotlib.pyplot as plt
import pandas as pd

def run_unified_simulation():
    print("=== Work Volatility Theory: Unified Simulation (Ch3-6) ===")
    model = UnifiedCSCTModel()
    
    steps = 300
    era_log = []
    
    print(f"Running {steps} steps across 3 Eras...")
    
    for i in range(steps):
        # Era Switching Logic
        if i < 100:
            model.era = "Legacy"
        elif i < 200:
            model.era = "Transition"
        else:
            model.era = "Optimized"
            
        model.step()
        era_log.append(model.era)
        
    print("Simulation Complete.")
    
    # Data Processing
    data = model.datacollector.get_model_vars_dataframe()
    data['Era'] = era_log
    
    # Visualization: The "Phase Shift" Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Verification of CSCT: From Legacy to Deep End Society', fontsize=16)
    
    # 1. Hamiltonian (Efficiency)
    axes[0,0].plot(data['Hamiltonian'], color='red')
    axes[0,0].set_title('Social Hamiltonian (Cost/Mismatch)')
    axes[0,0].set_ylabel('Energy')
    axes[0,0].axvline(100, linestyle='--', color='gray')
    axes[0,0].axvline(200, linestyle='--', color='gray')
    axes[0,0].text(20, data['Hamiltonian'].max()*0.9, "Legacy\n(Greedy)", color='gray')
    axes[0,0].text(120, data['Hamiltonian'].max()*0.9, "Transition\n(Deep End)", color='gray')
    
    # 2. Entropy (Order) - Ch3 Theory
    axes[0,1].plot(data['Entropy'], color='orange')
    axes[0,1].set_title('System Entropy (Chaos/Volatility)')
    axes[0,1].axvline(100, linestyle='--', color='gray')
    axes[0,1].axvline(200, linestyle='--', color='gray')
    axes[0,1].set_ylabel('S')
    
    # 3. Disputes (Legal) - Ch4 Theory
    axes[1,0].plot(data['Disputes'], color='black')
    axes[1,0].set_title('Legal Dispute Backlog')
    axes[1,0].axvline(100, linestyle='--', color='gray')
    axes[1,0].axvline(200, linestyle='--', color='gray')
    axes[1,0].set_ylabel('Cases')
    
    # 4. Trust & Wellbeing (Social) - Ch5/6
    axes[1,1].plot(data['Trust'], label='Social Trust', color='blue')
    axes[1,1].plot(data['Wellbeing'], label='Well-being', color='green', linestyle=':')
    axes[1,1].set_title('Trust & Well-being')
    axes[1,1].legend()
    axes[1,1].axvline(100, linestyle='--', color='gray')
    axes[1,1].axvline(200, linestyle='--', color='gray')
    
    plt.tight_layout()
    plt.savefig('unified_result.png')
    print("Saved unified_result.png")
    
    # Output Stats
    print("\n[Era Statistics]")
    for era in ["Legacy", "Transition", "Optimized"]:
        subset = data[data['Era'] == era]
        h_mean = subset['Hamiltonian'].mean()
        s_mean = subset['Entropy'].mean()
        t_mean = subset['Trust'].mean()
        print(f"Era: {era:<10} | H: {h_mean:<8.2f} | S: {s_mean:<8.2f} | Trust: {t_mean:<8.4f}")

if __name__ == "__main__":
    run_unified_simulation()
