import random

# --- Student Information Block ---
NAME = "CHETAN KANSAL"
USN = "1WA24CS094"

def calculate_conflicts(board):
    """Calculates the number of attacking queen pairs (conflicts)."""
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Check row alignment or diagonal alignment
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_successor(board):
    """Finds the highest-valued (lowest conflict) successor state."""
    current_conflicts = calculate_conflicts(board)
    best_board = list(board)
    best_conflicts = current_conflicts
    
    # Generate all possible neighbor states (4 columns x 3 alternative rows)
    for col in range(4):
        original_row = board[col]
        for row in range(4):
            if row == original_row:
                continue
            
            # Create neighbor state
            neighbor = list(board)
            neighbor[col] = row
            neighbor_conflicts = calculate_conflicts(neighbor)
            
            # Track the neighbor with the minimum conflicts
            if neighbor_conflicts < best_conflicts:
                best_conflicts = neighbor_conflicts
                best_board = neighbor
                
    return best_board, best_conflicts

def hill_climbing():
    # 1. Generate initial random state for 4 queens
    initial_state = [random.randint(0, 3) for _ in range(4)]
    initial_conflicts = calculate_conflicts(initial_state)
    
    current_state = list(initial_state)
    current_conflicts = initial_conflicts
    
    steps = 0
    while True:
        # 2. Find the highest-valued successor
        neighbor, neighbor_conflicts = get_best_successor(current_state)
        
        # 3. If neighbor value is not better than current, return current
        if neighbor_conflicts >= current_conflicts:
            break
            
        current_state = neighbor
        current_conflicts = neighbor_conflicts
        steps += 1
        
    return initial_state, initial_conflicts, current_state, current_conflicts, steps

# Run the algorithm
init_state, init_conflicts, solution, final_conflicts, total_steps = hill_climbing()

# --- Output Report ---
print("=========================================")
print(f"Name: {NAME}")
print(f"USN : {USN}")
print("=========================================")

print("\n--- Initial State ---")
print(f"Initial Board Array   : {init_state}")
print(f"Initial Conflicts     : {init_conflicts}")

print("\n--- Final Results ---")
print(f"Final Board Array     : {solution}")
print(f"Final Conflicts       : {final_conflicts}")
print(f"Total Steps taken     : {total_steps}")

if final_conflicts == 0:
    print("\nSuccess! A valid solution was found.")
else:
    print("\nStuck in a local minimum / plateau (No better neighbors).")
