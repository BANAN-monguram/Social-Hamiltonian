#include "model.h"
#include <time.h>

// Helper to generate random double 0.0 - 1.0
double rand_d() {
    return (double)rand() / RAND_MAX;
}

void init_agents(Agent agents[], int count) {
    for (int i = 0; i < count; i++) {
        agents[i].id = i;
        agents[i].is_busy = false;
        agents[i].current_task_id = -1;
        agents[i].stress = 0.0;
        
        // Distribute types: 10% Robot, 40% Human, 50% LLM
        double r = rand_d();
        if (r < 0.1) {
            agents[i].type = AGENT_ROBOT;
            agents[i].creativity = 0.1;
            agents[i].logic = 0.95;
            agents[i].physical = 0.9;
            agents[i].cost_per_tick = 5.0; // Maintenance
            agents[i].error_rate = 0.01;
            agents[i].max_stress = 1000.0; // Machines don't burnout easily
        } else if (r < 0.5) {
            agents[i].type = AGENT_HUMAN;
            agents[i].creativity = 0.9;
            agents[i].logic = 0.7;
            agents[i].physical = 0.6;
            agents[i].cost_per_tick = 20.0; // High living cost
            agents[i].error_rate = 0.05;
            agents[i].max_stress = 100.0;
        } else {
            agents[i].type = AGENT_LLM;
            agents[i].creativity = 0.6; // Stochastic
            agents[i].logic = 0.8;
            agents[i].physical = 0.0; // No body
            agents[i].cost_per_tick = 0.5; // Very cheap (Token cost)
            agents[i].error_rate = 0.1; // Hallucination
            agents[i].max_stress = 1000.0;
        }
    }
}

void init_tasks(Task tasks[], int count) {
    for (int i = 0; i < count; i++) {
        tasks[i].id = i;
        tasks[i].is_completed = false;
        tasks[i].assigned_agent_id = -1;
        tasks[i].difficulty = rand_d();
        
        double r = rand_d();
        if (r < 0.4) tasks[i].type = TASK_LOGIC;
        else if (r < 0.7) tasks[i].type = TASK_CREATIVE;
        else tasks[i].type = TASK_PHYSICAL;
    }
}

// Simple logic: Assign first available agent regardless of suitability
void assign_tasks_greedy(Agent agents[], int agent_count, Task tasks[], int task_count) {
    int task_idx = 0;
    for (int i = 0; i < agent_count; i++) {
        if (!agents[i].is_busy && task_idx < task_count) {
            agents[i].is_busy = true;
            agents[i].current_task_id = tasks[task_idx].id;
            tasks[task_idx].assigned_agent_id = agents[i].id;
            task_idx++;
        }
    }
}

// "Deep End" logic: Assign based on cost/capability match
void assign_tasks_optimized(Agent agents[], int agent_count, Task tasks[], int task_count) {
    // This is a simplified matching. In reality, this would be a min-cost max-flow or similar.
    // Here we iterate tasks and find best agent.
    
    for (int t = 0; t < task_count; t++) {
        if (tasks[t].is_completed) continue;
        
        int best_agent = -1;
        double min_score = 1000000.0; // Lower is better (Hamiltonian)
        
        for (int a = 0; a < agent_count; a++) {
            if (agents[a].is_busy) continue;
            
            // Calculate potential cost (H) for this pair
            double capability = 0.0;
            if (tasks[t].type == TASK_LOGIC) capability = agents[a].logic;
            else if (tasks[t].type == TASK_CREATIVE) capability = agents[a].creativity;
            else if (tasks[t].type == TASK_PHYSICAL) capability = agents[a].physical;
            
            // Penalty if capability is below difficulty
            double mismatch = (tasks[t].difficulty > capability) ? (tasks[t].difficulty - capability) * 100.0 : 0.0;
            
            // Cannot do physical if no body
            if (tasks[t].type == TASK_PHYSICAL && agents[a].physical < 0.1) mismatch = 10000.0;

            double score = agents[a].cost_per_tick + mismatch;
            
            // Human specific: well-being penalty reduction if task matches preference (simplified as high creativity)
            if (agents[a].type == AGENT_HUMAN && tasks[t].type == TASK_CREATIVE) {
                score -= 10.0; // Reward for creative work
            }
            
            if (score < min_score) {
                min_score = score;
                best_agent = a;
            }
        }
        
        if (best_agent != -1) {
            agents[best_agent].is_busy = true;
            agents[best_agent].current_task_id = tasks[t].id;
            tasks[t].assigned_agent_id = agents[best_agent].id;
        }
    }
}

double calculate_hamiltonian(Agent agents[], int agent_count, Task tasks[], int task_count) {
    double H = 0.0;
    
    // Sum of costs
    for (int i = 0; i < agent_count; i++) {
        if (agents[i].is_busy) {
            H += agents[i].cost_per_tick;
            
            // Check task result
            int tid = agents[i].current_task_id;
            // Success check (simplified)
            double capability = 0.0;
            if (tasks[tid].type == TASK_LOGIC) capability = agents[i].logic;
            else if (tasks[tid].type == TASK_CREATIVE) capability = agents[i].creativity;
            else if (tasks[tid].type == TASK_PHYSICAL) capability = agents[i].physical;
            
            if (rand_d() > capability) {
                 H += 50.0; // Penalty for failure
            }
        }
    }
    return H;
}

int main() {
    srand((unsigned int)time(NULL));
    
    Agent agents[NUM_AGENTS];
    Task tasks[NUM_TASKS];
    
    printf("--- Work Volatility Theory Simulation (Phase 1) ---\n");
    printf("Agents: %d, Tasks: %d\n\n", NUM_AGENTS, NUM_TASKS);
    
    // 1. Run Baseline (Greedy)
    init_agents(agents, NUM_AGENTS);
    init_tasks(tasks, NUM_TASKS);
    assign_tasks_greedy(agents, NUM_AGENTS, tasks, NUM_TASKS);
    double h_greedy = calculate_hamiltonian(agents, NUM_AGENTS, tasks, NUM_TASKS);
    printf("[Baseline] Hamiltonian (Total Cost): %.2f\n", h_greedy);
    
    // 2. Run Optimized (Deep End)
    init_agents(agents, NUM_AGENTS); // Reset
    init_tasks(tasks, NUM_TASKS);    // Reset
    assign_tasks_optimized(agents, NUM_AGENTS, tasks, NUM_TASKS);
    double h_opt = calculate_hamiltonian(agents, NUM_AGENTS, tasks, NUM_TASKS);
    printf("[DeepEnd]  Hamiltonian (Total Cost): %.2f\n", h_opt);
    
    double improvement = (h_greedy - h_opt) / h_greedy * 100.0;
    printf("\nImprovement: %.2f%%\n", improvement);
    
    return 0;
}
