import heapq
import sys
from collections import deque

# Hàm đọc dữ liệu từ file
def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    grid_size = eval(lines[0].strip())  # [rows, columns]
    start = eval(lines[1].strip())  # Vị trí bắt đầu
    goals = [eval(g.strip()) for g in lines[2].split('|')]  # Các vị trí đích
    walls = [eval(w.strip()) for w in lines[3:]]  # Các bức tường
    return grid_size, start, goals, walls

# Lớp Grid quản lý lưới và tường
class Grid:
    def __init__(self, rows, cols, walls):
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        # Đánh dấu các bức tường
        for wall in walls:
            x, y, w, h = wall
            for i in range(h):
                for j in range(w):
                    # Sử dụng đúng hệ tọa độ Cartesian, chuyển đổi thành chỉ số hàng và cột
                    if (y + i) < rows and (x + j) < cols:  # Kiểm tra hợp lệ
                        self.grid[y + i][x + j] = 1  # y là hàng, x là cột

    def is_wall(self, x, y):
        return self.grid[y][x] == 1  # Kiểm tra xem ô này có phải tường không

def dfs(grid, start, goals):
    stack = [(start, [])]  # Stack holds the current position and the path to it
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movements: right, left, down, up

    while stack:
        current, path = stack.pop()
        nodes_expanded += 1
        path = path + [current]

        # If a goal is found, return the path and number of expanded nodes
        if current in goals:
            return path, nodes_expanded

        # Expand the neighboring cells
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])

            # Check if the new position is within the grid, not visited, and not a wall
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                stack.append((next_pos, path))

    # If no path is found, return None and the number of expanded nodes
    return None, nodes_expanded


def bfs(grid, start, goals):
    queue = deque([(start, [])])
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movement directions: right, left, down, up
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        path = path + [current]


        # If a goal is found, return the path and the number of expanded nodes
        if current in goals:
            return path, nodes_expanded

        # Explore neighboring cells
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            
            # Check if the neighboring cell is valid (within grid bounds and not visited)
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                queue.append((next_pos, path))

    return None, nodes_expanded


# Hàm tính khoảng cách Manhattan
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# Function to calculate Manhattan distance
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# A* Search with 
def a_star(grid, start, goals):
    pq = []
    heapq.heappush(pq, (0, 0, start, []))
    visited = set([start])
    cost_from_start = {start: 0}
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible movements (right, left, down, up)

    while pq:
        # Get the cell with the lowest cost from the priority queue
        _, g, current, path = heapq.heappop(pq)
        nodes_expanded += 1
        path = path + [current]

        # If the goal is found, return the path and the number of expanded nodes
        if current in goals:
            return path, nodes_expanded

        # Explore neighboring cells
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            new_cost = g + 1  # Assume the movement cost between cells is 1
            if 0 <= next_pos[1] < len(grid.grid[0]) and 0 <= next_pos[0] < len(grid.grid) and not grid.is_wall(next_pos[0], next_pos[1]):
                if next_pos not in visited or new_cost < cost_from_start.get(next_pos, float('inf')):
                    cost_from_start[next_pos] = new_cost
                    priority = new_cost + min(manhattan_distance(next_pos, goal) for goal in goals)
                    heapq.heappush(pq, (priority, new_cost, next_pos, path))
                    visited.add(next_pos)


    # If no path is found, return None and the number of expanded nodes
    return None, nodes_expanded



# Greedy Best-First Search (GBFS)
def gbfs(grid, start, goals):
    pq = []
    heapq.heappush(pq, (0, start, []))  # Initialize priority queue with (heuristic, start, path)
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movement directions: right, left, down, up

    while pq:
        _, current, path = heapq.heappop(pq)  # Pop the node with the lowest heuristic
        nodes_expanded += 1
        path = path + [current]



        # Explore neighbors
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])

            # Boundary check is no longer needed here because is_wall() handles it
            if next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                # Priority based on Manhattan distance to the nearest goal
                priority = min(manhattan_distance(next_pos, goal) for goal in goals)
                heapq.heappush(pq, (priority, next_pos, path))


    # If no path is found, return None and the number of nodes expanded
    return None, nodes_expanded

# CUS1 - Iterative Deepening Search
def depth_limited_search(grid, current, goals, depth, path, visited):
    if depth == 0 and current in goals:
        return path + [current]
    
    if depth > 0:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]) and next_pos not in visited:
                visited.add(next_pos)
                path.append(current)
                
                
                result = depth_limited_search(grid, next_pos, goals, depth - 1, path, visited)
                
                # If we found a result, return it
                if result:
                    return result
                
    return None

def ids(grid, start, goals):
    depth = 0
    nodes_expanded = 0

    while True:
        visited = set([start])
        result = depth_limited_search(grid, start, goals, depth, [], visited)
        nodes_expanded += len(visited)
        if result:
            return result, nodes_expanded
        depth += 1




# Uniform Cost Search (CUS2)
def ucs(grid, start, goals):
    pq = []
    heapq.heappush(pq, (0, start, []))  # (cost, current_position, path)
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Four possible movements: right, left, down, up

    while pq:
        # Get the node with the lowest cumulative cost
        g, current, path = heapq.heappop(pq)
        path = path + [current]

        nodes_expanded += 1
        
        # Check if we have reached any goal
        if current in goals:
            return path, nodes_expanded

        # Explore the neighbors
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])

            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]):
                if next_pos not in visited:
                    visited.add(next_pos)
                    heapq.heappush(pq, (g + 1, next_pos, path))

    return None, nodes_expanded


# Run the chosen search algorithm
def main():
    if len(sys.argv) < 3:
        print("Usage: python sol.py <algorithm> <datafile>")
        sys.exit(1)

    algorithm = sys.argv[1].upper()  # Chosen algorithm
    filename = sys.argv[2]  # Data file name

    # Read data from the file
    grid_size, start, goals, walls = load_data(filename)
    grid = Grid(grid_size[0], grid_size[1], walls)  # Rows first, columns second

    # Run the chosen search algorithm
    if algorithm == "DFS": 
        path, nodes_expanded = dfs(grid, start, goals)
    elif algorithm == "DFS_GUI": 
        path, nodes_expanded = dfs(grid, start, goals)
    elif algorithm == "BFS":
        path, nodes_expanded = bfs(grid, start, goals)
    elif algorithm == "GBFS":
        path, nodes_expanded = gbfs(grid, start, goals)
    elif algorithm == "ASTAR":
        path, nodes_expanded = a_star(grid, start, goals)
    elif algorithm == "CUS1":
        path, nodes_expanded = ids(grid, start, goals)
    elif algorithm == "CUS2":
        path, nodes_expanded = ucs(grid, start, goals)
    else:
        print(f"Algorithm {algorithm} is not supported.")
        sys.exit(1)

    # Print the result to the terminal
    if path:
        print(f"Goal found at {path[-1]}")
        print(f"Number of nodes expanded: {nodes_expanded}")
        print(f"Path: {path}")
    else:
        print(f"No path to the goal found. Number of nodes expanded: {nodes_expanded}")


if __name__ == "__main__":
    main()
