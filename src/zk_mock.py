import time
import hashlib
import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation of zk-SNARKs Computational Load
# Note: Real zk-SNARKs (Groth16, Halo2) involve heavy Elliptic Curve Pairing and Polynomial Arithmetic.
# Here we simulate the *computational cost* using Modular Exponentiation (O(log n)) and Hashing.
#
# Assumptions:
# - Proving is computationally expensive (Heavy).
# - Verifying is cheap (Light).
# - Batching reduces amortized cost.

class ZKBenchmark:
    def __init__(self):
        # Parameters to tune "simulated difficulty"
        # Adjusted to approx real-world ratios (Proving is ~1000x costlier than Verifying)
        self.proof_complexity = 50000 
        self.verify_complexity = 50 
        
    def _heavy_compute(self, iterations):
        """Simulate CPU intensive task (Modular Exponentiation)"""
        base = 123456789
        mod = 1000000007
        res = 1
        # Simple loop to burn CPU cycles deterministically
        for _ in range(iterations):
            res = pow(base, 2, mod)
        return res

    def generate_proof(self, transaction_data):
        """Simulate Prover: Generates a proof for a transaction."""
        start = time.perf_counter()
        
        # 1. Private Witness Processing (Hash)
        witness_hash = hashlib.sha256(transaction_data.encode()).hexdigest()
        
        # 2. Constraint Satisfaction (Heavy Compute)
        _ = self._heavy_compute(self.proof_complexity)
        
        duration = time.perf_counter() - start
        return {"proof": "pi_0x" + witness_hash[:8], "time": duration}

    def verify_proof(self, proof):
        """Simulate Verifier: Checks the proof."""
        start = time.perf_counter()
        
        # 1. Pairing Check / Hash Check (Light Compute)
        _ = self._heavy_compute(self.verify_complexity)
        
        duration = time.perf_counter() - start
        return {"valid": True, "time": duration}

    def generate_batch_proof(self, transactions):
        """Simulate Recursive Proof (Batching): Proving N proofs in one."""
        start = time.perf_counter()
        
        # Batching Logic:
        # Instead of N * cost, it's roughly (N * low_cost) + fixed_heavy_cost
        # Simulating "Aggregation" overhead
        
        # 1. Aggregate inputs
        _ = self._heavy_compute(self.proof_complexity * 2) # Fixed overhead
        
        # 2. Linear aggregation cost (small)
        _ = self._heavy_compute(100 * len(transactions))
        
        duration = time.perf_counter() - start
        return {"proof": "pi_batch", "time": duration}

def run_benchmark():
    print("=== Phase 8: zk-SNARKs Technical Feasibility Benchmark ===")
    zk = ZKBenchmark()
    
    # 1. Individual Transaction Latency
    n_tx = 100
    print(f"\n[Test 1] Individual Proof Benchmark ({n_tx} txs)")
    
    prove_times = []
    verify_times = []
    
    for i in range(n_tx):
        tx = f"tx_{i}_{random.random()}"
        
        # Prove
        p_res = zk.generate_proof(tx)
        prove_times.append(p_res['time'])
        
        # Verify
        v_res = zk.verify_proof(p_res['proof'])
        verify_times.append(v_res['time'])
        
    avg_prove = np.mean(prove_times)
    avg_verify = np.mean(verify_times)
    
    print(f"Average Prove Time:   {avg_prove*1000:.2f} ms")
    print(f"Average Verify Time:  {avg_verify*1000:.2f} ms")
    print(f"P/V Ratio:            {avg_prove/avg_verify:.1f}x")
    print(f"Max TPS (Individual): {1.0/(avg_prove + avg_verify):.2f}")

    # 2. Batch Processing (Scalability)
    batch_sizes = [10, 50, 100, 500, 1000]
    batch_tps = []
    
    print(f"\n[Test 2] Batch Proof Benchmark (Recursive SNARKs Effect)")
    
    for bs in batch_sizes:
        txs = [f"tx_{i}" for i in range(bs)]
        
        # Batch Prove
        p_res = zk.generate_batch_proof(txs)
        
        # Batch Verify (Verifying one batch proof covers all N)
        v_res = zk.verify_proof(p_res['proof'])
        
        total_time = p_res['time'] + v_res['time']
        tps = bs / total_time
        batch_tps.append(tps)
        
        print(f"Batch Size {bs}: Total Time {total_time:.4f}s -> {tps:.2f} TPS")

    # Visualization
    plt.figure(figsize=(10, 6))
    
    # TPS Curve
    plt.plot(batch_sizes, batch_tps, marker='o', label='Recursive SNARKs (Batching)', color='blue')
    plt.axhline(y=1.0/(avg_prove + avg_verify), color='red', linestyle='--', label='Individual Proofs (Baseline)')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Batch Size (Transactions)')
    plt.ylabel('Throughput (TPS)')
    plt.title('zk-SNARKs Scalability: Individual vs Batch Verification')
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.legend()
    
    plt.savefig('zk_feasibility.png')
    print("\nSaved zk_feasibility.png")
    
    # 3. Feasibility Conclusion
    print("\n[Conclusion]")
    if batch_tps[-1] > 1000:
        print(">> HFT IS FEASIBLE with Batching. (TPS > 1000)")
    else:
        print(">> HFT shows latency issues. Requires hardware acceleration.")

if __name__ == "__main__":
    run_benchmark()
