
"""
Quantum Experiment Runner
=========================
Executes the full suite of experiments defined in the specification.

1. Benchmark Suite (Claim-A/B): Classical vs Hybrid on Max-Cut.
2. Grand Unified Suite (G-Claim): Outer Loop dynamics.
3. Visualization.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import json
from quantum_benchmarks import BenchmarkGenerator
from quantum_solvers import ClassicalSolver, SimulatedNISQSolver
from hybrid_engine import HybridSolver, ComparisonRunner
from grand_unified_experiment import OuterLoopSystem

OUTPUT_DIR = "quantum_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_benchmark_suite():
    print("=== Running Benchmark Suite (Claim A/B) ===")
    
    gen = BenchmarkGenerator(seed=42)
    runner = ComparisonRunner()
    
    results = []
    
    # Sweep N
    for n in [20, 30, 40, 60, 80, 100]:
        print(f"Benchmarking N={n}...")
        # Generate Instance
        prob = gen.generate_sparse_maxcut(n, avg_degree=4, cluster_prob=0.2)
        
        # Run Comparison
        res = runner.compare(prob)
        
        # Calculate Improvement
        e_c = res['Classical']['E']
        e_h = res['Hybrid']['E']
        if e_c != 0:
            imp = (e_c - e_h) / abs(e_c) * 100.0
        else:
            imp = 0.0
            
        results.append({
            'N': n,
            'Classical_E': e_c,
            'Hybrid_E': e_h,
            'Improvement_%': imp,
            'Win': res['HybridWin']
        })
        
    df = pd.DataFrame(results)
    print(df)
    df.to_json(os.path.join(OUTPUT_DIR, "benchmark_results.json"), orient="records", indent=4)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['N'], df['Improvement_%'], marker='o', linewidth=2, color='purple')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_xlabel('Problem Size (N)')
    ax.set_ylabel('Hybrid Improvement over Classical (%)')
    ax.set_title('Claim B: Hybrid vs Classical Performance (Simulated NISQ)')
    ax.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, "quantum_performance.png"))
    plt.close()

def run_grand_unified_test():
    print("=== Running Grand Unified Test (G-Claim) ===")
    
    system = OuterLoopSystem(n_agents=50)
    log_F, log_Trust = system.run(steps=200)
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:red'
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('System Frustration (Free Energy F)', color=color)
    ax1.plot(log_F, color=color, linewidth=2, label="F (Optimization)")
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Mean Social Trust', color=color)
    ax2.plot(log_Trust, color=color, linewidth=2, linestyle='--', label="Trust (Accumulation)")
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Grand Unified Algorithm: Simultaneous Optimization & Trust Building')
    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grand_unified_dynamics.png"))
    plt.close()
    
    # Save Data
    data = {"F": log_F, "Trust": log_Trust}
    with open(os.path.join(OUTPUT_DIR, "grand_unified_data.json"), "w") as f:
        json.dump(data, f, indent=4) # Custom dump for lists

if __name__ == "__main__":
    run_benchmark_suite()
    run_grand_unified_test()
    print(f"Experiments complete. Results saved to {os.path.abspath(OUTPUT_DIR)}")
