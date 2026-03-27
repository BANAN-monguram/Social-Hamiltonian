#ifndef MODEL_H
#define MODEL_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

// Tuning Parameters
#define NUM_AGENTS 100
#define NUM_TASKS 1000
#define TIME_STEPS 50

typedef enum {
    AGENT_HUMAN,
    AGENT_LLM,
    AGENT_ROBOT
} AgentType;

typedef enum {
    TASK_LOGIC,      // Requires precision (Robot/LLM good)
    TASK_CREATIVE,   // Requires creativity (Human good, LLM OK)
    TASK_PHYSICAL    // Requires physical body (Human/Robot good)
} TaskType;

typedef struct {
    int id;
    AgentType type;
    
    // Capabilities (0.0 - 1.0)
    double creativity;
    double logic;
    double physical;
    
    // Properties
    double cost_per_tick;   // Salary, electricity, API cost
    double error_rate;      // Probability of failure
    double stress;          // Accumulates for humans (Well-being inverse)
    double max_stress;      // Burnout threshold
    
    // Current State
    bool is_busy;
    int current_task_id;
} Agent;

typedef struct {
    int id;
    TaskType type;
    
    // Requirements (0.0 - 1.0)
    double difficulty;
    
    // Status
    bool is_completed;
    int assigned_agent_id;
} Task;

// Function Prototypes
void init_agents(Agent agents[], int count);
void init_tasks(Task tasks[], int count);
double calculate_hamiltonian(Agent agents[], int agent_count, Task tasks[], int task_count);
void assign_tasks_greedy(Agent agents[], int agent_count, Task tasks[], int task_count);
void assign_tasks_optimized(Agent agents[], int agent_count, Task tasks[], int task_count);

#endif // MODEL_H
