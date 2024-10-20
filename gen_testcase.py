import random

def create_grid(rows, cols):
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    return grid

def generate_random_walls(grid, num_walls, rows, cols):
    walls = []
    for _ in range(num_walls):
        w = random.randint(1, 3)
        h = random.randint(1, 3)
        x = random.randint(0, cols - w - 1)
        y = random.randint(0, rows - h - 1)
        for i in range(h):
            for j in range(w):
                grid[y + i][x + j] = '#'
        walls.append((y, x, h, w))
    return walls

def display_grid(grid):
    for y, row in enumerate(grid):
        row_str = ''.join(row)
        print(row_str)

def generate_random_goals(grid, num_goals, rows, cols):
    goals = []
    for _ in range(num_goals):
        while True:
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            if grid[y][x] == '.':
                grid[y][x] = 'G'
                goals.append((y, x))
                break
    return goals

def generate_maze(rows, cols, num_walls, num_goals):
    grid = create_grid(rows, cols)

    # Generate walls and goals
    walls = generate_random_walls(grid, num_walls, rows, cols)
    goals = generate_random_goals(grid, num_goals, rows, cols)

    # Set start position (ensure it's not a wall or a goal)
    while True:
        start_x = random.randint(0, cols - 1)
        start_y = random.randint(0, rows - 1)
        if grid[start_y][start_x] == '.':
            grid[start_y][start_x] = 'S'
            start = (start_y, start_x)
            break

    display_grid(grid)

    # Output the formatted test case without extra information
    print(f"[{rows},{cols}]")
    print(f"({start[1]},{start[0]})")  # Start position
    goals_str = ' | '.join([f"({g[1]},{g[0]})" for g in goals])
    print(goals_str)  # Goal positions
    for wall in walls:
        print(f"({wall[1]},{wall[0]},{wall[3]},{wall[2]})")  # Walls (x, y, w, h)

if __name__ == "__main__":
    # Example usage
    rows, cols = 10, 10  # Size of the grid
    num_walls = 5  # Number of walls
    num_goals = 2  # Number of goals
    generate_maze(rows, cols, num_walls, num_goals)
