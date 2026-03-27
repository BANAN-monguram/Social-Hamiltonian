import numpy as np
import matplotlib.pyplot as plt

def run_semantic_annealing():
    print("=== Physics Experiment 4: Semantic Annealing (Double Well) ===")
    
    # Parameters
    n_agents = 500
    steps = 100
    dt = 0.05
    noise_strength = 0.3 # T
    
    # Trajectories
    # Case 1: Rigid (Legacy)
    pos_rigid = np.full(n_agents, -1.0) # Start at Left Well (-1)
    avg_rigid = []
    
    # Case 2: Flexible (Intervention)
    pos_flex = np.full(n_agents, -1.0)
    avg_flex = []
    
    # Barrier Function (Double Well)
    # V(x) = a * (x^2 - 1)^2
    # F(x) = -dV/dx = -a * 2(x^2 - 1) * 2x = -4ax(x^2 - 1)
    
    def get_force(x, a):
        return -4 * a * x * (x**2 - 1)

    print("Simulating...")
    
    for t in range(steps):
        # 1. Rigid Simulation (Constant high barrier)
        a_rigid = 5.0 # Steep walls, High Rigidity
        force_r = get_force(pos_rigid, a_rigid)
        noise_r = np.random.normal(0, np.sqrt(noise_strength), n_agents)
        pos_rigid += force_r * dt + noise_r
        # Containment
        pos_rigid = np.clip(pos_rigid, -2.0, 2.0)
        avg_rigid.append(np.mean(pos_rigid))
        
        # 2. Flexible Simulation (Intervention at t=30-50)
        if 30 <= t <= 50:
            a_flex = 0.1 # Semantic Softening (Blurry Meaning) -> Low Barrier
        else:
            a_flex = 5.0 # Normal Rigidity
            
        force_f = get_force(pos_flex, a_flex)
        noise_f = np.random.normal(0, np.sqrt(noise_strength), n_agents)
        
        # Bias towards innovation (Right) when barrier is low
        # The "New Narrative" exerts a slight pull
        if 30 <= t <= 50:
            force_f += 0.5 
            
        pos_flex += force_f * dt + noise_f
        pos_flex = np.clip(pos_flex, -2.0, 2.0)
        avg_flex.append(np.mean(pos_flex))

    # Visualization
    plt.figure(figsize=(10, 6))
    
    # Plot Barrier Height (conceptual)
    barrier_profile = [5.0 if not (30 <= t <= 50) else 0.1 for t in range(steps)]
    
    plt.plot(avg_rigid, label='Legacy (Rigid Meaning)', color='gray', linestyle='--')
    plt.plot(avg_flex, label='Deep End (Semantic Intervention)', color='blue', linewidth=2)
    
    # Highlight Intervention Zone
    plt.axvspan(30, 50, color='yellow', alpha=0.2, label='Semantic Softening (Tunneling)')
    
    plt.title('Paradigm Shift via Meaning Softening (Double Well Potential)')
    plt.ylabel('Average Position (-1: Old, +1: New)')
    plt.xlabel('Time')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.text(10, -1.2, 'Old Paradigm', ha='center', color='red')
    plt.text(80, 1.2, 'New Paradigm', ha='center', color='green')
    
    plt.legend()
    plt.grid(True)
    plt.savefig('physics_semantic_annealing.png')
    print("Saved physics_semantic_annealing.png")

if __name__ == "__main__":
    run_semantic_annealing()
