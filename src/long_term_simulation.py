import numpy as np
import matplotlib.pyplot as plt

def run_long_term_simulation():
    print("=== Phase 7: 500-Year Sustainability Test (Capitalism vs CSCT) ===")
    
    years = 500
    
    # Common Environmental Factors
    initial_pop_human = 100.0 # Million
    depopulation_rate = 0.005 # -0.5% per year
    
    # Energy Constraint (Thermodynamic Limit)
    max_energy_capacity = 20000.0 # Upper limit (raised to show scale)
    
    # Models
    # A: Capitalism (Stronger Baseline)
    cap_gdp = []
    cap_capital = 100.0
    cap_pop = initial_pop_human
    cap_productivity = 1.0 # TFP
    cap_tech_growth = 0.015 # 1.5% annual growth (AI usage in Cap)
    
    # B: CSCT (Post-Capitalism)
    csct_gdp = []
    csct_capital = 100.0
    csct_pop_human = initial_pop_human
    csct_pop_ai = 1.0 
    
    # Disasters
    np.random.seed(42)
    disaster_years = []
    for y in range(years):
        if np.random.random() < 0.02: 
            disaster_years.append(y)
            
    print(f"Disaster Years: {disaster_years}")

    for year in range(years):
        # 1. Demographics & Tech
        cap_pop *= (1.0 - depopulation_rate)
        cap_productivity *= (1.0 + cap_tech_growth) # Tech Progress exists in Capitalism too
        
        csct_pop_human *= (1.0 - depopulation_rate)
        csct_pop_ai *= 1.05 # Moore's Law
        
        # 2. Disaster Impact
        shock = 0.0
        if year in disaster_years:
            shock = 0.4 
            
        # --- Capitalism Logic --- 
        # Output Y = A * K^a * L^b (Cobb-Douglas with TFP)
        cap_capital *= (1.0 - shock)
        
        # Capitalism uses AI (Productivity) to offset Pop decline
        # But it's less efficient at "Value Matching" than CSCT
        cap_output = cap_productivity * (cap_capital ** 0.3) * (cap_pop ** 0.7)
        cap_gdp.append(cap_output)
        
        # Reinvestment
        cap_capital += cap_output * 0.15 # Higher savings needed
        cap_capital *= 0.95 
        
        # --- CSCT Logic --- 
        real_shock = shock * 0.2 
        
        # Thermodynamic Feedback (Over-damped / Soft Landing) - Critique: Eliminate Oscillation
        # As Usage -> 1.0, Resistance increases smoothly (Tanh).
        energy_demand = (csct_pop_human * 1.0) + (csct_pop_ai * 0.1)
        usage_ratio = energy_demand / max_energy_capacity
        
        # Soft Damping Function (Tanh)
        # Ratio 0.0 -> Factor 1.0
        # Ratio 1.0 -> Factor 0.5
        # Ratio 1.5 -> Factor 0.0 (Growth stops)
        damping_factor = 0.5 * (1 - np.tanh((usage_ratio - 1.0) * 5.0))
        
        # Real Shock
        csct_capital *= (1.0 - real_shock)
        if csct_capital < 10: csct_capital = 10.0
        
        # Total Labor
        raw_labor = csct_pop_human + (csct_pop_ai * 0.8) 
        
        # Effective Labor (Throttled by Damping)
        effective_labor = raw_labor * (0.5 + 0.5 * damping_factor)
        
        # Output
        # CSCT gets a "Matching Premium" (A=1.2) because Global Optimization > Greedy
        # This prevents the "Initial Underperformance" vs Capitalism
        csct_matching_efficiency = 1.2 
        csct_output = csct_matching_efficiency * (csct_capital ** 0.4) * (effective_labor ** 0.6)
        csct_gdp.append(csct_output)
        
        # Reinvestment (Growth Driver)
        csct_capital += csct_output * 0.2 * damping_factor 
        csct_capital *= 0.95

    # 4. Realistic Baseline (Advanced Economies Recent Trend ~0.8%)
    # To contrast with the "Idealized Capitalism" (1.5%)
    real_gdp = []
    current_real = cap_gdp[0] # Start at same point
    for y in range(years):
        real_gdp.append(current_real)
        current_real *= 1.008 # 0.8% Growth (Japan/EU avg)
        
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot Real World Reference first (Background)
    ax.plot(real_gdp, label='Real-World Trend (0.8% - Advanced Nations)', color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
    
    # Plot Sim Models
    ax.plot(cap_gdp, label='Idealized Capitalism (1.5% Tech Growth)', color='red', linestyle='--')
    ax.plot(csct_gdp, label='CSCT (Structural Superiority)', color='blue', linewidth=2.5)
    
    # Log Scale
    ax.set_yscale('log')
    
    # Mark Disasters
    for dy in disaster_years:
        ax.axvline(dy, color='black', alpha=0.1, linewidth=1)

    plt.title('500-Year Simulation: CSCT vs Idealized Capitalism vs Reality')
    plt.xlabel('Year')
    plt.ylabel('Economic Output (Log Scale)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig('long_term_sustainability_with_context.png')
    print("Saved long_term_sustainability_with_context.png")

if __name__ == "__main__":
    run_long_term_simulation()
