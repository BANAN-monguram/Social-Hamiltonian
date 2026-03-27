
import os
import json
from advanced_stress_test_suite import run_experiment_A, benchmark_zk_snarks, run_experiment_C, run_experiment_D

def export_json():
    print("Running experiments and exporting to JSON...")
    
    # Run Experiment A
    df_a = run_experiment_A()
    df_a.to_json("results_experiment_a.json", orient="records", indent=4)
    print("Saved results_experiment_a.json")
    
    # Run Experiment B
    df_b = benchmark_zk_snarks()
    df_b.to_json("results_experiment_b.json", orient="records", indent=4)
    print("Saved results_experiment_b.json")
    
    # Run Experiment C
    df_c = run_experiment_C()
    df_c.to_json("results_experiment_c.json", orient="records", indent=4)
    print("Saved results_experiment_c.json")
    
    # Run Experiment D
    df_d = run_experiment_D()
    df_d.to_json("results_experiment_d.json", orient="records", indent=4)
    print("Saved results_experiment_d.json")

    print("\nAll exports complete.")

if __name__ == "__main__":
    export_json()
