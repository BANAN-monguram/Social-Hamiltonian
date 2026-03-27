# Social Hamiltonian and Legal Engineering: Simulation Audit Package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the simulation source code, parameter configurations, and raw empirical logs used to benchmark and verify the architectural claims made in the research paper **"Social Hamiltonian and Legal Engineering: A Constructive Approach to the Latent Torus Concept via Quantum Algorithms and Smart Contracts"**.

By open-sourcing this package, we grant researchers full access to reproduce the phase transition boundaries of the *Latent Torus*, verify the "Grand Unified Algorithm," and test the mathematical stress limits of the system independently.

## 📖 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Directory Structure](#2-directory-structure)
3. [Running the Simulations](#3-running-the-simulations)
   - [A. Macroscopic Multi-Agent Sim (Ch 3-6)](#a-macroscopic-multi-agent-sim-ch-3-6)
   - [B. Quantum Benchmark Proxy (Ch 5)](#b-quantum-benchmark-proxy-ch-5)
   - [C. zk-SNARKs Throughput Estimation (Ch 5)](#c-zk-snarks-throughput-estimation-ch-5)
   - [D. Semantic Annealing & Crash Test (Ch 7)](#d-semantic-annealing--crash-test-ch-7)
4. [Audit Logs & Verifiability](#4-audit-logs--verifiability)

---

## 1. Prerequisites

This package requires Python 3.10+ and standard scientific computing libraries. 
We strongly recommend using a virtual environment.

```bash
git clone [Insert GitHub URL]
cd simulation_audit_package
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

*(Note: The `quantum` simulations currently use a local "Noisy Thermal Sampling" proxy model to mimic NISQ devices. You do not need API access to actual Quantum Hardware to run these reproducibility benchmarks, though real-hardware extensions via D-Wave Ocean SDK or Qiskit can be drop-in replaced).*

---

## 2. Directory Structure

```text
simulation_audit_package/
━E├── src/                        # Core simulation Python scripts
━E  ├── macro_run.py            # HFT/ToJ Macro economy modeling
━E  ├── hybrid_engine.py        # NISQ + Classical local search loop
━E  ├── zk_mock.py              # Cryptographic throughput simulator
━E  └── ... 
━E├── c_impl/                     # C implementation of cost optimization
━E├── data/                       # Simulation outputs and visualizations
━E  ├── results/                # Raw JSON logs (quantum/stress)
━E  └── plots/                  # Generated benchmark charts
━E├── docs/                       # Refined research reports and summaries
━E├── experiment_log.txt          # Master chronological log of all Phase 1-8 experiments
├── quantum_spec_report.md      # Detailed analysis of the NISQ Hybrid benchmark claim
└── requirements.txt            # Python dependencies
```

---

## 3. Running the Simulations

### A. Macroscopic Multi-Agent Sim (Ch 3-6)
To verify the "Grand Unified Algorithm" behavior (where Trust $\tau$ increases while Free Energy $F$ drops), run the macro simulation:
```bash
python src/macro_run.py
```
> **Output Interpretation**: The script outputs the Hamiltonian and Trust metrics per era. You should observe the system transitioning from a high-entropy "Chaos" state to a stable "Negentropy" steady-state following the activation of the *Deep End* optimization.

### B. Quantum Benchmark Proxy (Ch 5)
To reproduce the sparse graph Max-Cut benchmarking (testing the 50-100 qubit regime):
```bash
python src/quantum_benchmarks.py
```
> **Output Interpretation**: Re-generates `data/results/quantum/benchmark_results.json`. Pay attention to $N=40$ through $N=60$. While purely classical algorithms win at $N=20$, the Hybrid model will sporadically secure improvements (e.g., +2.17%) in the middle scales, validating the paper's *feasible regime* claim.

### C. zk-SNARKs Throughput Estimation (Ch 5)
To reproduce the cryptographic scalability assertions:
```bash
python src/zk_mock.py
```
> **Output Interpretation**: Simulates Groth16 using modular exponentiation. It outputs the TPS scaling matrix. Without batching, throughput flatlines. With batching (e.g., 1000 proofs), amortized verification approaches 40,000 TPS on an assumed 64-core parallel array.

### D. Semantic Annealing & Crash Test (Ch 7)
To verify the "Latent Torus" fallback limits and Phase Transition failure points:
```bash
python src/stress_test.py
python src/physics_semantic_annealing.py
```
> **Output Interpretation**: The crash test will artificially push Task Load to 500% while decaying Trust $\tau$. You will witness an exact mathematical breaking point (usually around Trust < 0.03) where the Hamiltonian explodes, confirming the system's finite stability limits described in the text.

---

## 4. Audit Logs & Verifiability

For a complete history of the parameters used, the empirical tuning process, and the logic behind the "Legal Engineering" implementation, please consult the `experiment_log.txt`. 

We welcome pull requests for implementing the Hybrid Optimization Loop on real QPU hardware (e.g., IBM Quantum / D-Wave).

## License
MIT License. Feel free to fork and build upon this framework.
