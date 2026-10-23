import random
import math

# --- Student Information Block ---
# Replace these strings with your actual details
NAME = "YOUR_NAME_HERE"
USN = "YOUR_USN_HERE"

def calculate_energy(board):
    """Calculates the number of attacking queen pairs (conflicts)."""
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_neighbor(board):
    """Generates a neighbor state by randomly moving one queen to a new row."""
    neighbor = list(board)
    col = random.randint(0, 7)
    new_row = random.randint(0, 7)
    while new_row == board[col]:
        new_row = random.randint(0, 7)
    neighbor[col] = new_row
    return neighbor

def simulated_annealing():
    # 1. Generate and save the initial random state
    initial_state = [random.randint(0, 7) for _ in range(8)]
    initial_energy = calculate_energy(initial_state)
    
    current_state = list(initial_state)
    current_energy = initial_energy
    
    # Hyperparameters
    T = 1.0           
    alpha = 0.99      
    min_T = 0.00001   
    max_steps = 10000 
    
    step = 0
    while current_energy > 0 and T > min_T and step < max_steps:
        neighbor = get_neighbor(current_state)
        neighbor_energy = calculate_energy(neighbor)
        
        delta_e = neighbor_energy - current_energy
        
        if delta_e < 0:
            current_state = neighbor
            current_energy = neighbor_energy
        else:
            acceptance_probability = math.exp(-delta_e / T)
            if random.random() < acceptance_probability:
                current_state = neighbor
                current_energy = neighbor_energy
                
        T *= alpha
        step += 1
        
    return initial_state, initial_energy, current_state, current_energy, step

# Run the algorithm
init_state, init_energy, solution, final_energy, total_steps = simulated_annealing()

# --- Output Report ---
print("=========================================")
print(f"Name: {NAME}")
print(f"USN : {USN}")
print("=========================================")

print("\n--- Initial State ---")
print(f"Initial Board Array   : {init_state}")
print(f"Initial Conflicts     : {init_energy}")

print("\n--- Final Results ---")
print(f"Final Board Array     : {solution}")
print(f"Final Conflicts       : {final_energy}")
print(f"Total Steps taken     : {total_steps}")

if final_energy == 0:
    print("\nSuccess! A valid solution was found.")
else:
    print("\nFailed to converge. Try running the script again.")
