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
        for wall in walls:
            x, y, w, h = wall
            for i in range(h):
                for j in range(w):
                    self.grid[x + i][y + j] = 1  # Đánh dấu tường

    def is_wall(self, x, y):
        return self.grid[x][y] == 1

    def draw_grid(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                color = WHITE
                if self.grid[row][col] == 1:
                    color = GRAY
                pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_cell(self, screen, pos, color):
        pygame.draw.rect(screen, color, pygame.Rect(pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, pygame.Rect(pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Tìm kiếm DFS (sửa đổi để chạy từng bước một)
def dfs(grid, start, goals, screen):
    stack = [(start, [])]
    visited = set([start])
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        current, path = stack.pop()
        nodes_expanded += 1
        path = path + [current]
        
        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(0.3)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded
        
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                stack.append((next_pos, path))
    
    return None, nodes_expanded

# Tìm kiếm BFS (sửa đổi để chạy từng bước một)
def bfs(grid, start, goals, screen):
    queue = deque([(start, [])])
    visited = set([start])
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        path = path + [current]
        
        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(0.3)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded
        
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                queue.append((next_pos, path))
    
    return None, nodes_expanded

import heapq
import math

# Hàm tính khoảng cách Manhattan
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Greedy Best-First Search
def gbfs(grid, start, goals, screen):
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set([start])
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        _, current, path = heapq.heappop(pq)
        nodes_expanded += 1
        path = path + [current]

        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(0.3)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                priority = min(manhattan_distance(next_pos, goal) for goal in goals)
                heapq.heappush(pq, (priority, next_pos, path))

    return None, nodes_expanded

# A* Search
def a_star(grid, start, goals, screen):
    pq = []
    heapq.heappush(pq, (0, 0, start, []))
    visited = set([start])
    cost_from_start = {start: 0}
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        _, g, current, path = heapq.heappop(pq)
        nodes_expanded += 1
        path = path + [current]

        # Vẽ ô đang duyệt với màu xanh dương
        grid.draw_cell(screen, current, BLUE)
        pygame.display.flip()
        time.sleep(0.3)  # Tạm dừng một chút để quan sát

        if current in goals:
            return path, nodes_expanded

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            new_cost = g + 1  # Giả sử chi phí di chuyển giữa các ô là 1
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and not grid.is_wall(next_pos[0], next_pos[1]):
                if next_pos not in visited or new_cost < cost_from_start.get(next_pos, float('inf')):
                    cost_from_start[next_pos] = new_cost
                    priority = new_cost + min(manhattan_distance(next_pos, goal) for goal in goals)
                    heapq.heappush(pq, (priority, new_cost, next_pos, path))
                    visited.add(next_pos)

    return None, nodes_expanded



# Hàm chính để chạy từ dòng lệnh và vẽ với Pygame
def main():
    if len(sys.argv) < 3:
        print("Usage: python sol.py <algorithm> <datafile>")
        sys.exit(1)

    algorithm = sys.argv[1].upper()  # Thuật toán được chọn
    filename = sys.argv[2]  # Tên file dữ liệu

    # Đọc dữ liệu từ file
    grid_size, start, goals, walls = load_data(filename)
    grid = Grid(grid_size[0], grid_size[1], walls)

    # Khởi tạo Pygame
    pygame.init()
    screen = pygame.display.set_mode((grid_size[1] * CELL_SIZE, grid_size[0] * CELL_SIZE))
    pygame.display.set_caption("DFS/BFS Visualization")

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
    # Thêm CUS1, CUS2 nếu cần
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
