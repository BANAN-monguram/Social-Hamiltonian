import matplotlib.pyplot as plt
import pandas as pd
from unified_model import UnifiedCSCTModel

# Set style for academic publication
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

def generate_figures():
    print("Generating Thesis Figures...")
    
    # 1. Run Simulation
    model = UnifiedCSCTModel()
    era_log = []
    steps = 300
    
    for i in range(steps):
        if i < 100: model.era = "Legacy"
        elif i < 200: model.era = "Transition"
        else: model.era = "Optimized"
        model.step()
        era_log.append(model.era)
        
    data = model.datacollector.get_model_vars_dataframe()
    data['Era'] = era_log
    
    # Helper to draw vertical Era lines
    def draw_era_lines(ax):
        ax.axvline(100, linestyle='--', color='black', alpha=0.5, linewidth=1)
        ax.axvline(200, linestyle='--', color='black', alpha=0.5, linewidth=1)
        
        # Add labels
        y_lim = ax.get_ylim()
        y_txt = y_lim[1] - (y_lim[1]-y_lim[0])*0.05
        ax.text(50, y_txt, 'Legacy\n(Atomized)', ha='center', va='top', fontsize=10, style='italic')
        ax.text(150, y_txt, 'Deep End\n(Phase Shift)', ha='center', va='top', fontsize=10, style='italic')
        ax.text(250, y_txt, 'ToJ\n(Steady State)', ha='center', va='top', fontsize=10, style='italic')

    # --- Figure 1: Entropy Phase Shift (Ch3) ---
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(data['Entropy'], color='#d62728', linewidth=2, label='System Entropy $S(t)$')
    
    ax1.set_title('Negentropy Generation via Deep End')
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Social Entropy $S$ (Dimensionless)')
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    draw_era_lines(ax1)
    ax1.legend(loc='lower left')
    
    # Annotation for Negentropy
    s_start = data['Entropy'].iloc[99]
    s_end = data['Entropy'].iloc[199]
    # Point arrow lower down the curve (closer to s_end)
    arrow_tip_y = s_end + (s_start - s_end) * 0.3 
    # Move text down
    text_y = s_start * 0.75
    
    ax1.annotate('Negentropy\nGeneration', xy=(150, arrow_tip_y), xytext=(170, text_y),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))
    
    plt.tight_layout()
    plt.savefig('thesis_fig_entropy_shift.png')
    print("Saved thesis_fig_entropy_shift.png")

    # --- Figure 2: Hamiltonian & Trust (Ch5/6) ---
    fig2, ax1 = plt.subplots(figsize=(8, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Social Hamiltonian $H$', color=color)
    ax1.plot(data['Hamiltonian'], color=color, linewidth=1.5, label='Hamiltonian (Cost)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Social Trust $\\tau$', color=color)  # we already handled the x-label with ax1
    ax2.plot(data['Trust'], color=color, linewidth=2, linestyle='--', label='Social Trust')
    ax2.tick_params(axis='y', labelcolor=color)
    
    draw_era_lines(ax1)
    plt.title('Correlation of Cost Reduction and Trust Accumulation')
    fig2.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('thesis_fig_socio_economic.png')
    print("Saved thesis_fig_socio_economic.png")

if __name__ == "__main__":
    generate_figures()
