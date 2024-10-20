import sys
from collections import deque
import pygame
import time

# Kích thước ô trong lưới
CELL_SIZE = 40

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Màu vàng để vẽ đường đi sau khi hoàn thành
LIGHT_BLUE = (173, 216, 230)  # A lighter shade of blue for visited (closed) nodes

# Time
TIME_SLEEP = 0.1

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

    def draw_grid(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                color = WHITE
                if self.grid[row][col] == 1:
                    color = GRAY
                pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_cell(self, screen, pos, color):
        pygame.draw.rect(screen, color, pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Tìm kiếm DFS
def dfs(grid, start, goals, screen):
    stack = [(start, [])]
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while stack:
        current, path = stack.pop()
        nodes_expanded += 1
        path = path + [current]
        
        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded
        
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                stack.append((next_pos, path))
    
    return None, nodes_expanded

# Tìm kiếm DFS với trực quan hóa (tô màu cho backtracking giống BFS)
# def dfs(grid, start, goals, screen):
#     stack = [(start, [])]  # Stack holds the current position and the path to it
#     visited = set([start])
#     nodes_expanded = 0

#     moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movements: right, left, down, up

#     while stack:
#         current, path = stack.pop()
#         nodes_expanded += 1
#         path = path + [current]

#         # Vẽ ô đang duyệt với màu xanh dương (đang xét)
#         grid.draw_cell(screen, current, BLUE)
#         pygame.display.flip()
#         time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

#         # Nếu tìm thấy mục tiêu, trả về đường đi và số lượng nút đã mở rộng
#         if current in goals:
#             return path, nodes_expanded

#         # Flag to check if we are expanding any neighbors
#         expanded = False

#         # Mở rộng các ô lân cận
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])

#             # Kiểm tra xem ô mới có nằm trong lưới, chưa được thăm, và không phải là tường
#             if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
#                 visited.add(next_pos)
#                 stack.append((next_pos, path))

#                 # Vẽ ô lân cận được thêm vào stack (đang mở rộng)
#                 grid.draw_cell(screen, next_pos, BLUE)
#                 pygame.display.flip()
#                 time.sleep(TIME_SLEEP)

#                 expanded = True

#         # Nếu không mở rộng thêm được ô nào, nghĩa là đã backtrack xong
#         if not expanded:
#             grid.draw_cell(screen, current, LIGHT_BLUE)  # Đánh dấu ô đã duyệt xong
#             pygame.display.flip()
#             time.sleep(TIME_SLEEP)

#     # Nếu không tìm thấy đường đi, trả về None và số nút đã mở rộng
#     return None, nodes_expanded

# # Tìm kiếm BFS
# def bfs(grid, start, goals, screen):
#     queue = deque([(start, [])])
#     visited = set([start])
#     nodes_expanded = 0

#     moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
#     while queue:
#         current, path = queue.popleft()
#         nodes_expanded += 1
#         path = path + [current]
        
#         # Vẽ ô đang duyệt với màu xanh dương
#         grid.draw_cell(screen, current, BLUE)
#         pygame.display.flip()
#         time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

#         if current in goals:
#             return path, nodes_expanded
        
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
#             if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
#                 visited.add(next_pos)
#                 queue.append((next_pos, path))
    
#     return None, nodes_expanded

# BFS with Visualization
def bfs(grid, start, goals, screen):
    queue = deque([(start, [])])
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movement directions: right, left, down, up
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        path = path + [current]

        # Visualize the current cell being expanded in blue (active expansion)
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)  # Pause for visualization

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
                
                # Visualize the cell being added to the queue (active expansion)
                grid.draw_cell(screen, next_pos, BLUE)
                pygame.display.flip()
                time.sleep(TIME_SLEEP)

        # Visualize the fully explored (backtracked) cells in light blue
        grid.draw_cell(screen, current, LIGHT_BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)

    return None, nodes_expanded

import heapq

# Hàm tính khoảng cách Manhattan
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# A* Search
def a_star(grid, start, goals, screen):
    pq = []
    heapq.heappush(pq, (0, 0, start, []))
    visited = set([start])
    cost_from_start = {start: 0}
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while pq:
        _, g, current, path = heapq.heappop(pq)
        nodes_expanded += 1
        path = path + [current]

        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            new_cost = g + 1  # Giả sử chi phí di chuyển giữa các ô là 1
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]):
                if next_pos not in visited or new_cost < cost_from_start.get(next_pos, float('inf')):
                    cost_from_start[next_pos] = new_cost
                    priority = new_cost + min(manhattan_distance(next_pos, goal) for goal in goals)
                    heapq.heappush(pq, (priority, new_cost, next_pos, path))
                    visited.add(next_pos)

    return None, nodes_expanded

# Greedy Best-First Search
def gbfs(grid, start, goals, screen):
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while pq:
        _, current, path = heapq.heappop(pq)
        nodes_expanded += 1
        path = path + [current]

        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                priority = min(manhattan_distance(next_pos, goal) for goal in goals)
                heapq.heappush(pq, (priority, next_pos, path))

    return None, nodes_expanded


# # CUS1 - Iterative Deepening Search
# def depth_limited_search(grid, current, goals, depth, path, visited):
#     if depth == 0 and current in goals:
#         return path + [current]
#     if depth > 0:
#         moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
#             if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]) and next_pos not in visited:
#                 visited.add(next_pos)
#                 result = depth_limited_search(grid, next_pos, goals, depth - 1, path + [current], visited)
#                 if result:
#                     return result
#     return None

# def ids(grid, start, goals, screen):
#     depth = 0
#     nodes_expanded = 0

#     while True:
#         visited = set([start])
#         result = depth_limited_search(grid, start, goals, depth, [], visited)
#         nodes_expanded += len(visited)
#         if result:
#             return result, nodes_expanded
#         depth += 1
# CUS1 - Iterative Deepening Search with Visualization
# def depth_limited_search(grid, current, goals, depth, path, visited, screen):
#     if depth == 0 and current in goals:
#         return path + [current]
    
#     if depth > 0:
#         moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
            
#             if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]) and next_pos not in visited:
#                 visited.add(next_pos)
#                 path.append(current)
                
#                 # Visualize exploring node
#                 grid.draw_cell(screen, next_pos, BLUE)  
#                 pygame.display.flip()
#                 time.sleep(TIME_SLEEP)
                
#                 result = depth_limited_search(grid, next_pos, goals, depth - 1, path, visited, screen)
                
#                 # If we found a result, return it
#                 if result:
#                     return result
                
#                 # If not found, mark the node as fully explored (closed)
#                 grid.draw_cell(screen, next_pos, LIGHT_BLUE)
#                 pygame.display.flip()
#                 time.sleep(TIME_SLEEP)
                
#     return None

# def ids(grid, start, goals, screen):
#     depth = 0
#     nodes_expanded = 0

#     while True:
#         visited = set([start])
#         result = depth_limited_search(grid, start, goals, depth, [], visited, screen)
#         nodes_expanded += len(visited)
#         if result:
#             return result, nodes_expanded
#         depth += 1



# Constants for visualization

# CUS1 - Iterative Deepening Search with Visualization
def depth_limited_search(grid, current, goals, depth, path, visited, screen):
    if depth == 0 and current in goals:
        return path + [current]
    
    if depth > 0:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            
            if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]) and next_pos not in visited:
                visited.add(next_pos)
                path.append(current)
                
                # Visualize exploring node
                grid.draw_cell(screen, next_pos, BLUE)  
                pygame.display.flip()
                time.sleep(TIME_SLEEP)
                
                result = depth_limited_search(grid, next_pos, goals, depth - 1, path, visited, screen)
                
                # If we found a result, return it
                if result:
                    return result
                
                # If not found, mark the node as fully explored (closed)
                grid.draw_cell(screen, next_pos, LIGHT_BLUE)
                pygame.display.flip()
                time.sleep(TIME_SLEEP)
                
    return None

def ids(grid, start, goals, screen):
    depth = 0
    nodes_expanded = 0

    while True:
        visited = set([start])
        result = depth_limited_search(grid, start, goals, depth, [], visited, screen)
        nodes_expanded += len(visited)
        if result:
            return result, nodes_expanded
        depth += 1

# # CUS2 - Uniform Cost Search (UCS)
# def ucs(grid, start, goals, screen):
#     pq = []
#     heapq.heappush(pq, (0, start, []))
#     visited = set([start])
#     nodes_expanded = 0

#     moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

#     while pq:
#         g, current, path = heapq.heappop(pq)
#         nodes_expanded += 1
#         path = path + [current]

#         # Vẽ ô đang duyệt với màu xanh dương
#         grid.draw_cell(screen, current, BLUE)
#         pygame.display.flip()
#         time.sleep(TIME_SLEEP)  # Tạm dừng một chút để quan sát

#         if current in goals:
#             return path, nodes_expanded

#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
#             if 0 <= next_pos[1] < len(grid.grid) and 0 <= next_pos[0] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]):
#                 if next_pos not in visited:
#                     heapq.heappush(pq, (g + 1, next_pos, path))
#                     visited.add(next_pos)

#     return None, nodes_expanded



# Uniform Cost Search (CUS2) with Visualization
def ucs(grid, start, goals, screen):
    pq = []
    heapq.heappush(pq, (0, start, []))  # (cost, current_position, path)
    visited = set([start])
    nodes_expanded = 0

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Four possible movements: right, left, down, up

    while pq:
        # Get the node with the lowest cumulative cost
        g, current, path = heapq.heappop(pq)
        path = path + [current]

        # Visualize the node being expanded
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)

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

                    # Visualize adding to the priority queue
                    grid.draw_cell(screen, next_pos, BLUE)  # Blue for nodes being explored
                    pygame.display.flip()
                    time.sleep(TIME_SLEEP)

        # Visualize fully explored nodes (backtracking)
        grid.draw_cell(screen, current, LIGHT_BLUE)  # Light blue for closed nodes
        pygame.display.flip()
        time.sleep(TIME_SLEEP)

    return None, nodes_expanded


# Chạy thuật toán tìm kiếm theo lựa chọn
def main():
    if len(sys.argv) < 3:
        print("Usage: python sol.py <algorithm> <datafile>")
        sys.exit(1)

    algorithm = sys.argv[1].upper()  # Thuật toán được chọn
    filename = sys.argv[2]  # Tên file dữ liệu

    # Đọc dữ liệu từ file
    grid_size, start, goals, walls = load_data(filename)
    grid = Grid(grid_size[0], grid_size[1], walls)  # Hàng trước, cột sau

    # Khởi tạo Pygame
    pygame.init()
    screen = pygame.display.set_mode((grid_size[1] * CELL_SIZE, grid_size[0] * CELL_SIZE))
    pygame.display.set_caption("DFS/BFS/GBFS/A*/UCS Visualization")

    # Hiển thị lưới ban đầu
    screen.fill(WHITE)
    grid.draw_grid(screen)
    grid.draw_cell(screen, start, RED)  # Vẽ điểm bắt đầu
    for goal in goals:
        grid.draw_cell(screen, goal, GREEN)  # Vẽ các điểm đích
    pygame.display.flip()

    # Chạy thuật toán tìm kiếm theo lựa chọn
    if algorithm == "DFS":
        path, nodes_expanded = dfs(grid, start, goals, screen)
    elif algorithm == "BFS":
        path, nodes_expanded = bfs(grid, start, goals, screen)
    elif algorithm == "GBFS":
        path, nodes_expanded = gbfs(grid, start, goals, screen)
    elif algorithm == "ASTAR":
        path, nodes_expanded = a_star(grid, start, goals, screen)
    elif algorithm == "CUS1":
        path, nodes_expanded = ids(grid, start, goals, screen)
    elif algorithm == "CUS2":
        path, nodes_expanded = ucs(grid, start, goals, screen)
    else:
        print(f"Thuật toán {algorithm} không được hỗ trợ.")
        sys.exit(1)

    # In kết quả ra dòng lệnh
    if path:
        print(f"Đã tìm thấy mục tiêu tại {path[-1]}")
        print(f"Số lượng nút được mở rộng: {nodes_expanded}")
        print(f"Đường đi: {path}")
    else:
        print(f"Không tìm thấy đường đến mục tiêu. Số lượng nút được mở rộng: {nodes_expanded}")

    # Tô màu toàn bộ đường đi sau khi tìm thấy mục tiêu
    if path:
        for pos in path:
            grid.draw_cell(screen, pos, YELLOW)  # Tô màu đường đi bằng màu vàng
        pygame.display.flip()

    # Chờ người dùng đóng cửa sổ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()