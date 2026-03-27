# Social Hamiltonian and Legal Engineering: Simulation Audit Package

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

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
5. [Disclaimers & Limitations](#5-disclaimers--limitations)
6. [Note on Translation](#6-note-on-translation)
7. [License](#7-license)

---

## 1. Prerequisites

This package requires Python 3.10+ and standard scientific computing libraries. 
We strongly recommend using a virtual environment.

```bash
git clone https://github.com/BANAN-monguram/Social-Hamiltonian.git
cd Social-Hamiltonian
python -m venv venv
# On Windows: venv\Scripts\activate
# On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

*(Note: The `quantum` simulations currently use a local "Noisy Thermal Sampling" proxy model to mimic NISQ devices. You do not need API access to actual Quantum Hardware to run these reproducibility benchmarks).*

---

## 2. Directory Structure

```text
simulation_audit_package/
├── src/                        # Core simulation Python scripts
│   ├── macro_run.py            # HFT/ToJ Macro economy modeling
│   ├── hybrid_engine.py        # NISQ + Classical local search loop
│   └── ... 
├── c_impl/                     # C implementation of cost optimization
├── data/                       # Simulation outputs and visualizations
│   ├── results/                # Raw JSON logs (quantum/stress)
│   └── plots/                  # Generated benchmark charts
├── docs/                       # Refined research reports and summaries
├── main_en.pdf                 # Final Research Paper (English Manuscript)
├── experiment_log.txt          # Master chronological log of all Phase 1-8 experiments
└── requirements.txt            # Python dependencies
```

---

## 3. Running the Simulations

### A. Macroscopic Multi-Agent Sim (Ch 3-6)
To verify the "Grand Unified Algorithm" behavior, run the macro simulation:
```bash
python src/macro_run.py
```

### B. Quantum Benchmark Proxy (Ch 5)
To reproduce the sparse graph Max-Cut benchmarking (testing the 50-100 qubit regime):
```bash
python src/quantum_benchmarks.py
```

### C. zk-SNARKs Throughput Estimation (Ch 5)
To reproduce the cryptographic scalability assertions:
```bash
python src/zk_mock.py
```

### D. Semantic Annealing & Crash Test (Ch 7)
To verify the "Latent Torus" fallback limits and Phase Transition failure points:
```bash
python src/stress_test.py
python src/physics_semantic_annealing.py
```

---

## 4. Audit Logs & Verifiability

For a complete history of the parameters used and the logic behind the "Legal Engineering" implementation, please consult the `experiment_log.txt`. 

---

## 5. Disclaimers & Limitations
Please note that these simulations represent **stylized numerical thought experiments** designed to verify the internal consistency of the Social Hamiltonian theoretical framework. 
- **Idealized Assumptions**: The semantic intervention functions and cognitive response parameters in `src/` are exploratory proxies and have not been empirically derived from real-world longitudinal data.
- **Stochastic Variance**: Results may vary depending on the seed and environment.
- **Scientific Audit Only**: This package is intended for scholarly audit and conceptual validation.

---

## 6. Note on Translation
The English version of the associated research paper and this documentation was generated through a translation process from the original Japanese manuscript utilizing Large Language Models (LLMs). While rigorous efforts have been made to maintain scientific accuracy, the original author remains the final authority for the interpretation of the concepts discussed.

---

## 7. License
Distributed under the Apache License 2.0. See `LICENSE` for more information.
