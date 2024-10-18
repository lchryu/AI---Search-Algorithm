
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
BLUE = (0, 0, 255)  # Open nodes (being explored)
LIGHT_BLUE = (173, 216, 230)  # Closed nodes (already explored)
YELLOW = (255, 255, 0)  # Màu vàng để vẽ đường đi sau khi hoàn thành

# Time
TIME_SLEEP = 0.5

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

# Thuật toán BFS với tô màu
def bfs(grid, start, goals, screen):
    queue = deque([start])
    came_from = {start: None}
    expanded_nodes = 0
    
    while queue:
        current = queue.popleft()

        # Tô màu cho điểm đang mở rộng (closed nodes)
        grid.draw_cell(screen, current, LIGHT_BLUE)
        pygame.display.flip()
        time.sleep(TIME_SLEEP)

        if current in goals:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], expanded_nodes

        expanded_nodes += 1
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid.grid[0]) and 0 <= neighbor[1] < len(grid.grid):
                if not grid.is_wall(neighbor[0], neighbor[1]) and neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    
                    # Tô màu cho điểm đang được thêm vào hàng đợi (open nodes)
                    grid.draw_cell(screen, neighbor, BLUE)
                    pygame.display.flip()
                    time.sleep(TIME_SLEEP)
    
    return None, expanded_nodes

# Hàm chính
def main():
    filename = 'RobotNav-test_old.txt'  # Đổi tên file nếu cần
    algorithm = "BFS"  # Đổi thuật toán nếu cần
    
    grid_size, start, goals, walls = load_data(filename)
    grid = Grid(grid_size[0], grid_size[1], walls)  # Hàng trước, cột sau

    # Khởi tạo Pygame
    pygame.init()
    screen = pygame.display.set_mode((grid_size[1] * CELL_SIZE, grid_size[0] * CELL_SIZE))
    pygame.display.set_caption("BFS Visualization")

    # Hiển thị lưới ban đầu
    screen.fill(WHITE)
    grid.draw_grid(screen)
    grid.draw_cell(screen, start, RED)  # Vẽ điểm bắt đầu
    for goal in goals:
        grid.draw_cell(screen, goal, GREEN)  # Vẽ các điểm đích
    pygame.display.flip()

    # Chạy thuật toán BFS
    path, nodes_expanded = bfs(grid, start, goals, screen)

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
