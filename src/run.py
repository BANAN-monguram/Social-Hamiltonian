from model import CSCTModel
import numpy as np

def main():
    print("=== CSCT Simulation Phase 1: Cost Optimization ===\n")
    
    # Parameters
    NUM_HUMANS = 40
    NUM_LLMS = 50
    NUM_ROBOTS = 10
    NUM_TASKS = 100
    
    print(f"Agents: Humans={NUM_HUMANS}, LLMs={NUM_LLMS}, Robots={NUM_ROBOTS}")
    print(f"Tasks: {NUM_TASKS}\n")
    
    # Run Baseline
    model = CSCTModel(NUM_HUMANS, NUM_LLMS, NUM_ROBOTS, NUM_TASKS)
    h_greedy = model.run_allocation_greedy()
    print(f"[Baseline (Greedy)]")
    print(f"  Hamiltonian (Total Social Cost): {h_greedy:.2f}")
    
    # Run Optimized
    # Re-using same task set logic but inside model it regenerates random values if re-init
    # To be fair, we use the methods on the same model instance (tasks are stored)
    h_opt = model.run_allocation_optimized()
    print(f"[Deep End (Optimized)]")
    print(f"  Hamiltonian (Total Social Cost): {h_opt:.2f}")
    
    # Result
    improvement = (h_greedy - h_opt) / h_greedy * 100.0
    print(f"\nOptimization Improvement: {improvement:.2f}%")
    
    if improvement > 0:
        print("\n[Conclusion] The Grand Unified Algorithm successfully reduced social cost.")
        print("This validates the effectiveness of assigning tasks based on comparative advantage (e.g. LLMs for logic/rote, Humans for creativity).")
    else:
        print("\n[Conclusion] Optimization failed or baseline was already optimal.")

if __name__ == "__main__":
    main()
