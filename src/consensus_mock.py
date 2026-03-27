import numpy as np
import matplotlib.pyplot as plt

# Simulation of Civic Consensus: Democracy vs Proof of Trust vs Populism Dampening
# Based on Eq. 69 (Opinion Dynamics) and Eq. 78 (Dampener).

class ConsensusSim:
    def __init__(self, n_agents=1000):
        self.n_agents = n_agents
        
        # Agent Properties
        # Trust: Power Law distribution (Pareto Principle)
        # 20% have 80% of trust (Elites/Experts), 80% have low trust.
        self.trust_scores = np.random.pareto(a=2.0, size=n_agents)
        self.trust_scores /= np.sum(self.trust_scores) # Normalize
        
        # Opinions: -1.0 to 1.0 (Continuous)
        # Initial state: Random noise
        self.opinions = np.random.uniform(-0.5, 0.5, n_agents)
        
    def step(self, K_coupling, use_trust_weight=False, use_dampener=False):
        """
        Evolve opinions based on Ising-like interaction.
        sigma_i(t+1) = tanh( h_i + K * sum(sigma_j) )
        """
        
        # Mean Field Approximation for calculation speed
        # The "Social Field" Omega is the average opinion felt by everyone.
        if use_trust_weight:
            # Weighted by Trust (Proof of Trust)
            mean_opinion = np.sum(self.opinions * self.trust_scores)
        else:
            # Simple Average (1-Person-1-Vote Democracy)
            mean_opinion = np.mean(self.opinions)
            
        # Global Field Strength (Effective Influence)
        # Omega = K * Mean_Opinion
        # If Dampener is ON, K is reduced if Omega is too strong (Panic/Fanaticism)
        
        effective_K = K_coupling
        if use_dampener:
            # Eq. 78: K_corrected = K / (1 + gamma * |Omega|^2)
            # "Cooling down the heat of the mob"
            field_strength = abs(mean_opinion)
            gamma = 10.0 # Sensitivity
            effective_K = K_coupling / (1.0 + gamma * (field_strength ** 2))
            
        # Update everyone (mean field interaction)
        # Add some random noise (individuality)
        noise = np.random.normal(0, 0.1, self.n_agents)
        
        # Main Logic: Everyone is pulled towards the Mean
        # New Opinion = tanh( K * Mean + Self + Noise )
        # Using a slight inertia (0.8 previous + 0.2 new)
        field_force = effective_K * mean_opinion
        new_opinions = np.tanh(field_force + noise)
        
        self.opinions = 0.9 * self.opinions + 0.1 * new_opinions
        
        return mean_opinion, effective_K

def run_consensus_experiment():
    print("=== Phase 8b: Consensus & Populism Dampening Test ===")
    
    steps = 100
    K_panic = 3.0 # High internal coupling (Panic/Viral Phase)
    
    # Scenario 1: Direct Democracy + Panic (Mob Rule)
    sim1 = ConsensusSim()
    hist1 = []
    # Induce a small bias to trigger the avalanche
    sim1.opinions += 0.05 
    
    for _ in range(steps):
        m, _ = sim1.step(K_panic, use_trust_weight=False, use_dampener=False)
        hist1.append(m)
        
    print(f"Scenario 1 (Democracy+Panic): Final Opinion = {hist1[-1]:.2f} (Extreme Polarization)")

    # Scenario 2: Proof of Trust (Elites moderate, but still susceptible if elites panic?)
    sim2 = ConsensusSim()
    hist2 = []
    sim2.opinions += 0.05
    
    for _ in range(steps):
        m, _ = sim2.step(K_panic, use_trust_weight=True, use_dampener=False)
        hist2.append(m)
        
    print(f"Scenario 2 (Proof of Trust):  Final Opinion = {hist2[-1]:.2f} (Weighted)")

    # Scenario 3: CSCT Dampener (The Solution)
    sim3 = ConsensusSim()
    hist3 = []
    k_hist = []
    sim3.opinions += 0.05
    
    for _ in range(steps):
        m, k = sim3.step(K_panic, use_trust_weight=True, use_dampener=True)
        hist3.append(m)
        k_hist.append(k)
        
    print(f"Scenario 3 (CSCT Dampener):   Final Opinion = {hist3[-1]:.2f} (Restored Rationality)")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(hist1, label='1-Person-1-Vote (Mob Rule)', color='red', linestyle='--')
    ax1.plot(hist2, label='Proof of Trust (Weighted)', color='orange')
    ax1.plot(hist3, label='CSCT w/ Dampener (Rational)', color='blue', linewidth=2)
    ax1.set_title('Opinion Polarization under Panic (K=3.0)')
    ax1.set_ylabel('Average Opinion (-1 to 1)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(k_hist, label='Effective K (Coupling)', color='green')
    ax2.set_title('Dampener Activation (Auto-Cooling)')
    ax2.set_ylabel('Coupling Strength K')
    ax2.set_xlabel('Time Step')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('consensus_dampening.png')
    print("Saved consensus_dampening.png")

if __name__ == "__main__":
    run_consensus_experiment()
