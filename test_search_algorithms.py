import random

def generate_test_case(grid_size, start, goals_count, walls_count):
    goals = [(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(goals_count)]
    walls = [(random.randint(0, grid_size-2), random.randint(0, grid_size-2), random.randint(1, 3), random.randint(1, 3)) for _ in range(walls_count)]
    return grid_size, start, goals, walls

# Example usage
grid_size = 10
start = (0, 0)
test_case = generate_test_case(grid_size, start, 3, 5)
print(test_case)