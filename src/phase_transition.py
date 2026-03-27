from physics_engine import PhysicsModel
import matplotlib.pyplot as plt
import numpy as np

def run_phase_transition():
    print("=== Physics Experiment 2: Phase Transition & Finite Size Scaling ===")
    
    temps = np.linspace(0.1, 10.0, 20)
    sizes = [50, 100]
    
    plt.figure(figsize=(10, 6))
    
    for N in sizes:
        print(f"Simulating Size N={N}...")
        order_params = []
        
        for T in temps:
            # Run simulation at temperature T
            model = PhysicsModel(num_agents=N, temperature=T, coupling=1.0)
            # Equilibration
            for _ in range(50): model.step()
            
            # Measurement
            avg_order = 0
            for _ in range(20):
                model.step()
                avg_order += model.calculate_order_param()
            order_params.append(avg_order / 20.0)
            
        plt.plot(temps, order_params, marker='o', label=f"N={N}")
        
    plt.title('Phase Transition: Order Parameter vs Temperature')
    plt.xlabel('Temperature (Volatility)')
    plt.ylabel('Order Parameter (Coherence)')
    plt.legend()
    plt.grid(True)
    plt.savefig('physics_phase_transition.png')
    print("Saved physics_phase_transition.png")

if __name__ == "__main__":
    run_phase_transition()
