
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# Import the experiment functions
from advanced_stress_test_suite import run_experiment_A, benchmark_zk_snarks, run_experiment_C, run_experiment_D

def generate_figures():
    # Setup
    output_dir = "stress_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Use a default style
    plt.style.use('default') 
    
    # ==============================================================================
    # 1. Plot Experiment A (Semantic Hacking)
    # ==============================================================================
    print("Generating Plot A (Semantic Hacking)...")
    df_a = run_experiment_A()
    
    # Comparison: Final_H for Baseline vs Defense across Attack types
    attacks = df_a['Attack'].unique()
    conditions = df_a['Condition'].unique()
    
    # Prepare data for bar chart
    baseline_h = df_a[df_a['Condition'] == 'Baseline']['Final_H'].values
    defense_h = df_a[df_a['Condition'] == 'Defense']['Final_H'].values
    x = np.arange(len(attacks))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, baseline_h, width, label='Baseline', color='#d62728', alpha=0.7)
    rects2 = ax.bar(x + width/2, defense_h, width, label='Defense (Proposed)', color='#2ca02c', alpha=0.7)
    
    ax.set_xlabel('Attack Scenario')
    ax.set_ylabel('Social Cost (Hamiltonian)')
    ax.set_title('Impact of Semantic Attacks: Defense Effectiveness')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks, rotation=15)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add labels
    ax.bar_label(rects1, padding=3, fmt='%.0f')
    ax.bar_label(rects2, padding=3, fmt='%.0f')
    
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, 'adv_exp_a_semantic_hacking.png'))
    plt.close(fig)
    
    # ==============================================================================
    # 2. Plot Experiment B (zk-SNARKs)
    # ==============================================================================
    print("Generating Plot B (zk-SNARKs)...")
    df_b = benchmark_zk_snarks()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Log-Log Plot for Latency vs TPS
    ax.plot(df_b['Latency(64Core_ms)'], df_b['TPS(Est)'], marker='o', linestyle='-', linewidth=2, color='#1f77b4')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Latency (ms) [Log Scale]')
    ax.set_ylabel('Throughput (TPS) [Log Scale]')
    ax.set_title('zk-SNARKs Trade-off: Latency vs TPS (by Batch Size)')
    
    # Annotate points with Batch Size
    for i, row in df_b.iterrows():
        ax.annotate(f"n={int(row['BatchSize'])}", 
                    (row['Latency(64Core_ms)'], row['TPS(Est)']),
                    textcoords="offset points", xytext=(0,10), ha='center')
        
    ax.grid(True, which="both", ls="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, 'adv_exp_b_zk_benchmark.png'))
    plt.close(fig)

    # ==============================================================================
    # 3. Plot Experiment C (Oracle Risk)
    # ==============================================================================
    print("Generating Plot C (Oracle Risk)...")
    df_c = run_experiment_C()
    
    # Grouped Bar Chart
    noise_levels = df_c['NoiseLevel'].unique()
    x = np.arange(len(noise_levels))
    width = 0.35
    
    err_no_fb = df_c['Errors(NoFallback)'].values
    err_fb = df_c['Errors(Fallback)'].values
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, err_no_fb, width, label='No Fallback', color='#ff7f0e', alpha=0.8)
    rects2 = ax.bar(x + width/2, err_fb, width, label='With Fallback', color='#17becf', alpha=0.8)
    
    ax.set_xlabel('Sensor Noise Level (Probability)')
    ax.set_ylabel('Misjudgment Count (Errors)')
    ax.set_title('Oracle Risk Mitigation: Analog Fallback')
    ax.set_xticks(x)
    ax.set_xticklabels(noise_levels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, 'adv_exp_c_oracle_risk.png'))
    plt.close(fig)

    # ==============================================================================
    # 4. Plot Experiment D (Trust Bottleneck)
    # ==============================================================================
    print("Generating Plot D (Trust Bottleneck)...")
    df_d = run_experiment_D()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_d['Trust(tau)'], df_d['T_total'], marker='s', linestyle='-', color='#d62728', linewidth=2)
    
    ax.set_xlabel('Social Trust Level (tau)')
    ax.set_ylabel('Total Resolution Time (Arbitrary Units)')
    ax.set_title('The Trust Bottleneck: Why Tech alone cannot solve delay')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add text annotation
    ax.text(0.5, 500, 'Low Trust = Infinite Delay\n(Regardless of Compute Speed)', fontsize=10, color='red')
    
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, 'adv_exp_d_trust_bottleneck.png'))
    plt.close(fig)
    
    print(f"Done. Images saved to {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    generate_figures()
