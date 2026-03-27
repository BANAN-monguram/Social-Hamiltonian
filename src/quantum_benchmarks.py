
"""
Quantum Experiment Benchmarks
=============================
Generates problem instances for the Quantum Algorithm Limits experiment.
Focus: Sparse Max-Cut (Ising/QUBO)

Classes:
- BenchmarkGenerator: Creates graph instances.
- ProblemInstance: Holds the graph and QUBO matrix.
"""

import numpy as np
import networkx as nx

class ProblemInstance:
    def __init__(self, name, graph, qubo_matrix, optimal_value=None):
        self.name = name
        self.graph = graph
        self.qubo = qubo_matrix # Q matrix (numpy)
        self.n = len(graph.nodes)
        self.optimal_value = optimal_value # Optional, for normalization

class BenchmarkGenerator:
    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed)

    def generate_sparse_maxcut(self, n, avg_degree=4, cluster_prob=0.0):
        """
        Generates a Max-Cut problem on a sparse graph.
        If cluster_prob > 0, uses Stochastic Block Model (SBM) to add community structure.
        Otherwise, uses Erdos-Renyi.
        """
        if cluster_prob > 0:
            # Stochastic Block Model (2 communities)
            sizes = [n // 2, n - n // 2]
            # p_in > p_out to form clusters
            # avg_degree = (n/2 * p_in) + (n/2 * p_out) approx
            # Let's say p_in = 3 * p_out
            p_out = avg_degree / (2 * n) # Approximate
            p_in = p_out * (1.0 + cluster_prob * 3.0) 
            probs = [[p_in, p_out], [p_out, p_in]]
            G = nx.stochastic_block_model(sizes, probs, seed=self.seed)
        else:
            # Erdos-Renyi
            p = avg_degree / (n - 1)
            G = nx.erdos_renyi_graph(n, p, seed=self.seed)
        
        # Ensure standard labeling 0..n-1
        G = nx.convert_node_labels_to_integers(G)
        
        # Max-Cut -> QUBO
        # Maximize Cut = Maximize sum_{(i,j) in E} (1 - s_i s_j) / 2
        # where s_i in {-1, 1}
        # In QUBO x_i in {0, 1}, s_i = 2x_i - 1
        # Minimizing Hamiltonian H = sum_{(i,j) in E} s_i s_j
        
        # We construct Q for Minimization: x^T Q x
        # H_ising = sum J_ij s_i s_j
        # J_ij = 1 for edges.
        # s_i s_j = (2x_i - 1)(2x_j - 1) = 4x_i x_j - 2x_i - 2x_j + 1
        # We want to MINIMIZE sum s_i s_j
        # So we MINIMIZE sum (4 x_i x_j - 2 x_i - 2 x_j)
        
        Q = np.zeros((n, n))
        for i, j in G.edges:
            # Off-diagonal: 4
            # We split it 2 and 2 for symmetric or just 4 upper triangular
            # Let's use upper triangular for standard QUBO solvers
            u, v = min(i, j), max(i, j)
            Q[u, v] += 4.0
            
            # Diagonal: -2 per edge incident
            Q[u, u] -= 2.0
            Q[v, v] -= 2.0
            
        instance_name = f"MaxCut_N{n}_D{avg_degree}_C{cluster_prob}"
        return ProblemInstance(instance_name, G, Q)

    def generate_tokenized_work_instance(self, n_events, n_slots):
        """
        Generates a simplified 'Tokenized Work' recording problem.
        Select n_slots events from n_events to maximize total priority 
        under constraint of conflicting transactions.
        """
        # Simplified to Maximum Weighted Independent Set (MWIS) on a conflict graph
        # Or Knapsack-like.
        # Let's use MWIS on random conflict graph.
        
        # 1. Generate Events with Importance (Weights)
        weights = np.random.uniform(1.0, 10.0, n_events)
        
        # 2. Generate Conflicts (e.g., Double Spending, Time overlap)
        # Create a random conflict graph
        G = nx.erdos_renyi_graph(n_events, p=0.1, seed=self.seed)
        
        # Goal: Maximize sum w_i x_i subject to x_i + x_j <= 1 for (i,j) in E
        # Penalty formulation: Minimize -sum w_i x_i + P * sum x_i x_j
        
        P = max(weights) * 2.0 # Penalty factor
        
        Q = np.zeros((n_events, n_events))
        
        # Linear terms (diagonal) -> -weights
        for i in range(n_events):
            Q[i, i] = -weights[i]
            
        # Quadratic terms (conflicts) -> +P
        for i, j in G.edges:
            u, v = min(i, j), max(i, j)
            Q[u, v] += P
            
        return ProblemInstance(f"TokenWork_N{n_events}", G, Q)
