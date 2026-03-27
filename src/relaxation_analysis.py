from physics_engine import PhysicsModel
import matplotlib.pyplot as plt
import numpy as np

def run_relaxation_experiment():
    print("=== Physics Experiment 1: Relaxation Time Analysis ===")
    
    steps = 100
    shock_time = 10
    
    # 1. Configs
    configs = [
        {"name": "Legacy (Atomized)", "J": 0.1, "T": 2.0},
        {"name": "Deep End (Optimized)", "J": 2.0, "T": 0.5} # Lower Temp due to Trust
    ]
    
    plt.figure(figsize=(10, 6))
    
    for conf in configs:
        print(f"Running {conf['name']}...")
        model = PhysicsModel(coupling=conf['J'], temperature=conf['T'])
        energies = []
        
        for t in range(steps):
            # SHOCK at t=10
            if t == shock_time:
                # Move the 'Cheeseburger' (Task) to a new location
                model.current_task = np.array([10.0, 10.0])
                
            model.step()
            energies.append(model.calculate_hamiltonian())
            
        plt.plot(energies, label=f"{conf['name']} (J={conf['J']})", linewidth=2)

    plt.axvline(shock_time, color='red', linestyle='--', label='Shock Event')
    plt.title('Relaxation Dynamics: Response to External Shock')
    plt.xlabel('Time (Langevin Steps)')
    plt.ylabel('System Energy (Mismatch)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('physics_relaxation.png')
    print("Saved physics_relaxation.png")

if __name__ == "__main__":
    run_relaxation_experiment()
