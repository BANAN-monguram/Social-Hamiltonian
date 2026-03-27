import numpy as np
import matplotlib.pyplot as plt

# Simulation of "Living as Labor" (Ontological Value)
# Hypothesis based on "Model Collapse" theory (Shumailov et al., 2023):
# - AI training on AI data leads to collapse (Entropy -> 0).
# - Human data is needed to inject "Novelty" (Entropy > 0).
# - Thus, "Just Living" (generating novel data) is an economically valuable act (Labor).

def run_value_estimation():
    print("=== Phase 8c: Value of Entropy (Living as Labor) ===")
    
    generations = 50
    n_samples = 1000
    
    # 1. Pure AI Economy (Recursive Training)
    # Start with a rich distribution (Real World)
    data_dist = np.random.normal(0, 1.0, n_samples)
    
    ai_diversity = []
    
    for g in range(generations):
        # AI learns from current data and generates new data
        # AI tends to output the "Mean" or "Mode" -> Variance shrinks
        # We model this as: New Data = Model(Old Data) + small_noise
        # But 'small_noise' from AI is algorithmic (pseudo-random), not thermodynamic (true random).
        
        # Train: Find mean/std
        mu, sigma = np.mean(data_dist), np.std(data_dist)
        
        # Generate: (Model Collapse effect: sigma decreases)
        # "The tails are cut off"
        new_sigma = sigma * 0.95 
        data_dist = np.random.normal(mu, new_sigma, n_samples)
        
        ai_diversity.append(new_sigma)
        
    print(f"Scenario 1 (Pure AI): Final Diversity = {ai_diversity[-1]:.4f} (Model Collapse)")

    # 2. Hybrid Economy (Human-in-the-Loop)
    # Humans inject "Living Entropy" (Novelty)
    # Even if they don't "Work" (Logic), they "Live" (Experience/Emotion -> Data).
    
    data_dist_h = np.random.normal(0, 1.0, n_samples)
    human_diversity = []
    
    injection_rate = 0.1 # 10% data comes from Humans "Just Living"
    human_entropy_quality = 1.0 # Humans maintain the original variance
    
    for g in range(generations):
        mu, sigma = np.mean(data_dist_h), np.std(data_dist_h)
        
        # AI Generation
        n_ai = int(n_samples * (1 - injection_rate))
        ai_data = np.random.normal(mu, sigma * 0.95, n_ai)
        
        # Human Injection ("Living")
        n_human = n_samples - n_ai
        # Humans are weird: They generate outliers (Heavy Tails)
        human_data = np.random.normal(mu, human_entropy_quality, n_human) 
        
        # Mix
        data_dist_h = np.concatenate([ai_data, human_data])
        
        human_diversity.append(np.std(data_dist_h))
        
    print(f"Scenario 2 (With Humans): Final Diversity = {human_diversity[-1]:.4f} (Sustainable)")
    
    # 3. Valuation
    # Value V is proportional to Diversity D (Capability to handle novel situations)
    # Fair Wage = Contribution to D.
    
    value_sustained = human_diversity[-1]
    value_collapsed = ai_diversity[-1]
    net_value_of_humans = value_sustained - value_collapsed
    
    print(f"Net Value of Human Entropy: {net_value_of_humans:.4f}")
    print(">> This justifies 'Basic Income' as a 'Data Maintenance Fee'.")

    # Visualization
    plt.figure(figsize=(10, 6))
    
    plt.plot(ai_diversity, label='Pure AI Economy (Model Collapse)', color='red', linestyle='--')
    plt.plot(human_diversity, label='Hybrid Economy (Living = Labor)', color='blue', linewidth=2)
    
    plt.title('Why "Living" has Value: Prevention of Model Collapse')
    plt.xlabel('AI Generations')
    plt.ylabel('System Diversity (Entropy/Capability)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('value_of_living.png')
    print("Saved value_of_living.png")

if __name__ == "__main__":
    run_value_estimation()
