# import sys
# from collections import deque

# # Hàm đọc dữ liệu từ file
# def load_data(filename):
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#     grid_size = eval(lines[0].strip())  # [rows, columns]
#     start = eval(lines[1].strip())  # Vị trí bắt đầu
#     goals = [eval(g.strip()) for g in lines[2].split('|')]  # Các vị trí đích
#     walls = [eval(w.strip()) for w in lines[3:]]  # Các bức tường
#     return grid_size, start, goals, walls

# # Lớp Grid quản lý lưới và tường
# class Grid:
#     def __init__(self, rows, cols, walls):
#         self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
#         for wall in walls:
#             x, y, w, h = wall
#             for i in range(h):
#                 for j in range(w):
#                     self.grid[x + i][y + j] = 1  # Đánh dấu tường

#     def is_wall(self, x, y):
#         return self.grid[x][y] == 1

# # Tìm kiếm DFS
# def dfs(grid, start, goals):
#     stack = [(start, [])]
#     visited = set([start])
#     nodes_expanded = 0

#     moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
#     while stack:
#         current, path = stack.pop()
#         nodes_expanded += 1
#         path = path + [current]
        
#         if current in goals:
#             return path, nodes_expanded
        
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
#             if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
#                 visited.add(next_pos)
#                 stack.append((next_pos, path))
    
#     return None, nodes_expanded

# # Tìm kiếm BFS
# def bfs(grid, start, goals):
#     queue = deque([(start, [])])
#     visited = set([start])
#     nodes_expanded = 0

#     moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
#     while queue:
#         current, path = queue.popleft()
#         nodes_expanded += 1
#         path = path + [current]
        
#         if current in goals:
#             return path, nodes_expanded
        
#         for move in moves:
#             next_pos = (current[0] + move[0], current[1] + move[1])
#             if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
#                 visited.add(next_pos)
#                 queue.append((next_pos, path))
    
#     return None, nodes_expanded

# # Cài đặt thuật toán khác tại đây (GBFS, A*...)

# # Hàm chính để chạy từ dòng lệnh
# def main():
#     if len(sys.argv) < 3:
#         print("Usage: python sol.py <algorithm> <datafile>")
#         sys.exit(1)

#     algorithm = sys.argv[1].upper()  # Thuật toán được chọn
#     filename = sys.argv[2]  # Tên file dữ liệu

#     # Đọc dữ liệu từ file
#     grid_size, start, goals, walls = load_data(filename)
#     grid = Grid(grid_size[0], grid_size[1], walls)

#     # Chạy thuật toán tìm kiếm theo lựa chọn
#     if algorithm == "DFS":
#         path, nodes_expanded = dfs(grid, start, goals)
#     elif algorithm == "BFS":
#         path, nodes_expanded = bfs(grid, start, goals)
#     # elif thêm các thuật toán khác...
#     else:
#         print(f"Thuật toán {algorithm} không được hỗ trợ.")
#         sys.exit(1)

#     # In kết quả ra dòng lệnh
#     if path:
#         print(f"Đã tìm thấy mục tiêu tại {path[-1]}")
#         print(f"Số lượng nút được mở rộng: {nodes_expanded}")
#         print(f"Đường đi: {path}")
#     else:
#         print(f"Không tìm thấy đường đến mục tiêu. Số lượng nút được mở rộng: {nodes_expanded}")

# if __name__ == "__main__":
#     main()



import sys
from collections import deque
import pygame

# Kích thước ô trong lưới
CELL_SIZE = 40

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

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

    def draw_path(self, screen, path, start, goals):
        for pos in path:
            pygame.draw.rect(screen, BLUE, pygame.Rect(pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Vẽ điểm bắt đầu và mục tiêu
        pygame.draw.rect(screen, RED, pygame.Rect(start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for goal in goals:
            pygame.draw.rect(screen, GREEN, pygame.Rect(goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Tìm kiếm DFS
def dfs(grid, start, goals):
    stack = [(start, [])]
    visited = set([start])
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        current, path = stack.pop()
        nodes_expanded += 1
        path = path + [current]
        
        if current in goals:
            return path, nodes_expanded
        
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                stack.append((next_pos, path))
    
    return None, nodes_expanded

# Tìm kiếm BFS
def bfs(grid, start, goals):
    queue = deque([(start, [])])
    visited = set([start])
    nodes_expanded = 0

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        path = path + [current]
        
        if current in goals:
            return path, nodes_expanded
        
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < len(grid.grid) and 0 <= next_pos[1] < len(grid.grid[0]) and next_pos not in visited and not grid.is_wall(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                queue.append((next_pos, path))
    
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

    # Chạy thuật toán tìm kiếm theo lựa chọn
    if algorithm == "DFS":
        path, nodes_expanded = dfs(grid, start, goals)
    elif algorithm == "BFS":
        path, nodes_expanded = bfs(grid, start, goals)
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

    # Hiển thị quá trình tìm kiếm và đường đi
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        grid.draw_grid(screen)
        if path:
            grid.draw_path(screen, path, start, goals)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
