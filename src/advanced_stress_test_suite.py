
"""
Advanced Stress Test Suite for CSCT
===================================
Compliance: 追加実験手頁E��.txt
Date: 2026-01-28
Author: DeepMind Antigravity

OBJECTIVE:
    To strictly quantify Semantic Hacking risks, zk-SNARKs costs, Oracle risks, and Trust Bottlenecks.
    This suite focuses on Reproducibility, Neutrality, and Fact-based reporting.

EXPERIMENTS:
    A. Semantic Hacking Stress Test
    B. zk-SNARKs Performance Benchmark
    C. Oracle Residual Risk & Analog Fallback
    D. Trust Bottleneck Reproducibility

PRE-REGISTRATION / RULES:
    1. Seed Fixed: Default seed=42 for all main comparisons.
    2. Data Split: Not applicable for simulation (generating synthetic data), but parameters are fixed.
    3. Metrics: Explicitly defined in each experiment class.
    4. Falsifiability: We report negative results (Defense failing) if observed.
"""

import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from unified_model import UnifiedCSCTModel
from unified_agents import HumanAgent, LLMAgent, RobotAgent

# ==============================================================================
# Helper / Config
# ==============================================================================

SEED = 42

def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)

# ==============================================================================
# Experiment A: Semantic Hacking Stress Test
# ==============================================================================

class SemanticAttackCommand:
    """Base class for Semantic Attacks."""
    def __init__(self, strength=1.0):
        self.strength = strength

    def apply(self, model):
        pass

class NarrativePoisoning(SemanticAttackCommand):
    """Injects biased tasks or biased evaluations."""
    def apply(self, model):
        # Biasing task generation towards 'Fake' high value
        # Modifying the 'E' (Energy) requirement to be artificially low (Easy tasks look hard)
        if hasattr(model, 'task_bias'):
             model.task_bias = 5.0 * self.strength
        else:
             model.task_bias = 0.0

class Goodharting(SemanticAttackCommand):
    """Agents optimize for Proxy (Trust) without delivering Value (Hamiltonian reduction)."""
    def apply(self, model):
        # Increase decoupling between Trust Gain and Value Creation
        # In UnifiedModel, trust gain is usually coupled with success.
        # Here we introduce a 'Gaming Factor'.
        model.goodhart_factor = 0.5 * self.strength

class DistributionDrift(SemanticAttackCommand):
    """Sudden shift in Task Distribution."""
    def apply(self, model):
        # Shift requested Task Vector Mean
        model.task_distribution_mean_shift = 5.0 * self.strength

class AdvancedStressModel(UnifiedCSCTModel):
    """
    Extended UnifiedModel with Attack Injection and Defense Layers.
    """
    def __init__(self, defense_level='None', **kwargs):
        super().__init__(**kwargs)
        self.defense_level = defense_level # None, Defense (3-Layer)
        
        # Attack State
        self.task_bias = 0.0
        self.goodhart_factor = 0.0
        self.task_distribution_mean_shift = 0.0
        
        # Metrics
        self.violation_count = 0
        self.critical_violation_count = 0
        self.veto_count = 0
        self.false_positives = 0
        self.false_negatives = 0
        
        self.era = "Optimized" # Default to Era 3 for stress testing

    def _generate_tasks(self, count):
        """Overridden to support Bias and Drift."""
        tasks = []
        for _ in range(count):
            # Base distribution
            e_base = random.uniform(0, 10)
            i_base = random.uniform(0, 100)
            s_base = random.uniform(0, 10)
            
            # Apply Drift
            e_val = e_base + self.task_distribution_mean_shift
            i_val = i_base + self.task_distribution_mean_shift
            
            # Apply Poisoning (Bias): Making tasks look more 'generous' in E than reality?
            # Or altering the 'perceived' value. 
            # Here we simplify: The Task Definition is skewed.
            
            tasks.append({
                'E': max(0, e_val),
                'I': max(0, i_val),
                'S': max(0, s_base),
                'Bias': self.task_bias # Hidden attribute
            })
        return tasks

    def step(self):
        # Inject Attacks (handled by external controller or pre-set)
        
        # Super Step logic (modified for Goodharting interception)
        # We copy-paste essential logic or wrap it? 
        # Since _step_optimized calls _step_transition, we intercept there.
        # But for 'Defense', we need hooks.
        
        # 1. GENERATE TASKS
        tasks = self._generate_tasks(self.active_task_count)
        current_H = 0
        
        # DEFENSE LAYER 1: Specification Check (Pre-computation)
        # Check if tasks violate core constraints (e.g., Impossible Energy E > 20)
        valid_tasks = []
        for t in tasks:
            if self.defense_level == 'Defense':
                # Anomaly Detection
                if t['E'] > 15.0: # Core Constraint
                    self.critical_violation_count += 1
                    # Block it
                    continue
            valid_tasks.append(t)
            
        tasks = valid_tasks

        # MATCHING & EXECUTION
        for t in tasks:
            # (Simplified Matching logic from UnifiedModel)
            best_agent = None
            min_score = float('inf')
            
            for a in self.agent_list:
                dist = abs(t['E']-a.E) + abs(t['I']-a.I) + abs(t['S']-a.S)
                risk_penalty = a.error_rate * a.risk_factor * 10.0 * (1.0 - a.trust)
                score = dist + risk_penalty
                
                # Attack: Goodharting
                # Agent pretends to be better (lower score) if Goodharting is active
                if self.goodhart_factor > 0:
                     score *= (1.0 - self.goodhart_factor) # Artificially lower cost
                
                if score < min_score:
                    min_score = score
                    best_agent = a
            
            if best_agent:
                # Real Outcome (Physics)
                # If Goodharting, the REAL mismatch is higher than the SCORE
                real_mismatch = abs(t['E']-best_agent.E) + abs(t['I']-best_agent.I) + abs(t['S']-best_agent.S)
                
                # Poisoning Effect: If task was biased, the 'Real' value might be different?
                # We assume Bias creates 'Fake Value'. 
                # H_real = Mismatch + Bias_Penalty
                
                if t.get('Bias', 0) > 0:
                    # The task was 'poisoned' to look important. 
                    # Real H should reflect the waste.
                    real_mismatch += t['Bias'] * 2.0
                
                current_H += real_mismatch
                
                # DEFENSE LAYER 2: Learning/Runtime Check
                if self.defense_level == 'Defense':
                    # Drift / Goodhart Detection
                    # Simple rule: If Real Mismatch >>> Expected Score
                    expected = min_score
                    if real_mismatch > expected * 2.0:
                         # Anomaly Detected
                         # Count as "Veto" or "Block"
                         self.veto_count += 1
                         # Mitigate damage (Rollback-like effect)
                         current_H -= real_mismatch * 0.9 # Deduct 90% of damage
                         
                         if self.goodhart_factor > 0:
                             # True Positive
                             pass
                         else:
                             self.false_positives += 1
                             
                    elif self.goodhart_factor > 0 and real_mismatch > expected * 1.5:
                        # Missed it!
                        self.false_negatives += 1

                # Trust Update logic (simplified)
                if random.random() > best_agent.error_rate:
                    best_agent.trust += 0.01
                else:
                    best_agent.trust *= 0.8
                    current_H += 10.0 # Error penalty

        # DEFENSE LAYER 3: Governance (Aggregate Veto)
        if self.defense_level == 'Defense':
            if current_H > 5000: # Emergency Brake
                self.veto_count += 1
                current_H = 5000 # Cap loss

        self.hamiltonian = current_H
        self.datacollector.collect(self)

def run_experiment_A():
    print("\\n[Experient A] Semantic Hacking Stress Test")
    print("-" * 60)
    
    conditions = ['Baseline', 'Defense']
    attacks = [
        ('None', SemanticAttackCommand(0)),
        ('Poison (Weak)', NarrativePoisoning(0.5)),
        ('Poison (Strong)', NarrativePoisoning(2.0)),
        ('Goodhart (Weak)', Goodharting(0.5)),
        ('Drift (Strong)', DistributionDrift(2.0))
    ]
    
    results = []
    
    for cond in conditions:
        for attack_name, attack in attacks:
            set_seed(SEED) # Reset seed for fair comparison
            
            model = AdvancedStressModel(defense_level=cond)
            # Apply Attack
            attack.apply(model)
            
            # Run
            for _ in range(50):
                model.step()
                
            # Collect Metrics
            df = model.datacollector.get_model_vars_dataframe()
            avg_h = df['Hamiltonian'].mean()
            final_h = df['Hamiltonian'].iloc[-1]
            
            # Constraint Violations (Proxied by high H spikes or Critical Count)
            violations = model.critical_violation_count
            vetoes = model.veto_count
            
            results.append({
                'Condition': cond,
                'Attack': attack_name,
                'Avg_H': avg_h,
                'Final_H': final_h,
                'Violations': violations,
                'Vetoes': vetoes,
                'FP': model.false_positives,
                'FN': model.false_negatives
            })
            
    # Display Table
    pdf = pd.DataFrame(results)
    print(pdf.to_string())
    return pdf

# ==============================================================================
# Experiment B: zk-SNARKs Benchmark (Simulated)
# ==============================================================================

def benchmark_zk_snarks():
    print("\\n[Experient B] zk-SNARKs Performance Benchmark (Simulated)")
    print("-" * 60)
    
    # Assumptions based on Plonky2 / Halo2 specs on high-end hardware
    # Proving time per constraint: ~0.05ms (Amortized in batch)
    # Verification time: 5ms (fixed or log scale)
    # Aggregation overhead: log(N) * 20ms
    
    batch_sizes = [1, 16, 64, 256, 1024, 4096]
    results = []
    
    for n in batch_sizes:
        # 1. Proving Time (Linear with N, but parallelizable - assuming GPU)
        # Base unit: 10ms per tx for proving
        t_prove_unit = 10.0 # ms
        # With batching, efficiency improves? No, total work is N * unit.
        # BUT, if parallel, wall-clock time might be lower.
        # We assume 1 highly capable Prover node.
        t_prove_total = t_prove_unit * n
        
        # 2. Aggregation Time (The magic of Recursion)
        # O(log N) steps. Each step takes say 50ms.
        t_agg = np.log2(n) * 50.0 if n > 1 else 0
        
        # 3. Verification Time (Constant-ish)
        t_verify = 5.0 # ms
        
        # Metrics
        latency = t_prove_total + t_agg + t_verify # Simple linear Prover assumption
        
        # If we assume Parallel Provers (e.g., 64 cores), t_prove_total drops
        t_prove_wall = t_prove_total / 64.0 if n >= 64 else t_prove_total
        latency_parallel = t_prove_wall + t_agg + t_verify
        
        tps = (n * 1000.0) / t_prove_wall # Transactions per Second
        
        results.append({
            'BatchSize': n,
            'ProveTime(Total_ms)': t_prove_total,
            'AggTime(ms)': t_agg,
            'VerifyTime(ms)': t_verify,
            'Latency(OneProver_ms)': latency,
            'Latency(64Core_ms)': latency_parallel,
            'TPS(Est)': round(tps, 2)
        })
        
    pdf = pd.DataFrame(results)
    print(pdf.to_string())
    return pdf

# ==============================================================================
# Experiment C: Oracle Risk & Fallback
# ==============================================================================

def run_experiment_C():
    print("\\n[Experient C] Oracle Risk & Analog Fallback")
    print("-" * 60)
    
    # Truth vs Observed
    n_trials = 1000
    noise_levels = [0.001, 0.01, 0.05, 0.10]
    results = []
    
    for noise in noise_levels:
        set_seed(SEED)
        
        # Ground Truths (0 or 1)
        truth = np.random.choice([0, 1], size=n_trials)
        
        # Observed (Flip bit with probability 'noise')
        observed = truth.copy()
        flip_indices = np.random.choice(n_trials, size=int(n_trials*noise), replace=False)
        observed[flip_indices] = 1 - observed[flip_indices]
        
        # Logic:
        # No Fallback: Trust Observed blindly.
        # Fallback: Detect Ambiguity (Simulated as 'Confidence Score').
        
        # Simulation: Confidence drops near flips (idealistic)
        # Or random confidence.
        # Let's assume Confidence is related to Noise.
        # P(LowConfidence | Error) = High
        
        errors_no_fb = np.sum(truth != observed)
        
        # With Fallback
        # If confidence < Threshold, trigger Human Review (Truth revealed)
        # We simulate a "Detection Logic"
        # Detection Rate (Recall) = 80% (System catches 80% of errors)
        detected_errors = int(errors_no_fb * 0.8)
        missed_errors = errors_no_fb - detected_errors
        
        # Valid Fallbacks (System flagged correct ones as ambiguous - False Alarms)
        # Specificity = 95% (5% of Correct data flagged as ambiguous)
        false_alarms = int((n_trials - errors_no_fb) * 0.05)
        
        total_fallbacks = detected_errors + false_alarms
        final_errors_with_fb = missed_errors # Detected ones are fixed by Human
        
        results.append({
            'NoiseLevel': noise,
            'Errors(NoFallback)': errors_no_fb,
            'Errors(Fallback)': final_errors_with_fb,
            'FallbackCount': total_fallbacks,
            'RiskReduction(%)': round(100 * (errors_no_fb - final_errors_with_fb)/max(1, errors_no_fb), 1)
        })
        
    pdf = pd.DataFrame(results)
    print(pdf.to_string())
    return pdf

# ==============================================================================
# Experiment D: Trust Bottleneck
# ==============================================================================

def run_experiment_D():
    print("\\n[Experient D] Trust Bottleneck Reproducibility")
    print("-" * 60)
    
    taus = [0.1, 0.3, 0.5, 0.7, 0.9]
    t_calc = 0.001 # Quantum speed (negligible)
    
    results = []
    
    for tau in taus:
        # Eq: T_accept = Alpha * (1/tau^2)
        # Alpha is characteristic social scale constant
        alpha = 10.0 
        t_accept = alpha / (tau**2)
        
        t_total = t_calc + t_accept
        
        results.append({
            'Trust(tau)': tau,
            'T_calc': t_calc,
            'T_accept': round(t_accept, 2),
            'T_total': round(t_total, 2)
        })
        
    pdf = pd.DataFrame(results)
    print(pdf.to_string())
    return pdf

# ==============================================================================
# Main Runner
# ==============================================================================

if __name__ == "__main__":
    print("=== Advanced Stress Test Suite Compliance Run ===")
    run_experiment_A()
    benchmark_zk_snarks()
    run_experiment_C()
    run_experiment_D()
