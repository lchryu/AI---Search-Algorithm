from config import *
import pygame

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
