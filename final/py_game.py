import pygame

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Kích thước ô vuông
TILE_SIZE = 50

# Hàm đọc dữ liệu từ file
def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    grid_size = eval(lines[0].strip())  # [rows, columns]
    start = eval(lines[1].strip())  # Vị trí bắt đầu
    goals = [eval(g.strip()) for g in lines[2].split('|')]  # Các vị trí đích
    walls = [eval(w.strip()) for w in lines[3:]]  # Các bức tường
    return grid_size, start, goals, walls

# Hàm vẽ lưới với Pygame
def draw_grid(screen, grid_size, start, goals, walls):
    rows, cols = grid_size
    
    # Vẽ nền
    screen.fill(WHITE)

    # Vẽ từng ô
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # Vẽ các bức tường
    for wall in walls:
        x, y, w, h = wall
        for i in range(h):
            for j in range(w):
                pygame.draw.rect(screen, GRAY, ((y + j) * TILE_SIZE, (x + i) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Vẽ vị trí bắt đầu (robot)
    pygame.draw.rect(screen, RED, (start[1] * TILE_SIZE, start[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Vẽ các vị trí đích (goals)
    for goal in goals:
        pygame.draw.rect(screen, GREEN, (goal[1] * TILE_SIZE, goal[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Hàm chính để chạy Pygame
def main():
    # Đọc dữ liệu từ file
    filename = 'RobotNav-test.txt'  # Thay bằng file của bạn
    grid_size, start, goals, walls = load_data(filename)

    # Khởi tạo Pygame
    pygame.init()
    screen_width = grid_size[1] * TILE_SIZE
    screen_height = grid_size[0] * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Robot Navigation Grid")

    # Chạy vòng lặp Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Vẽ lưới
        draw_grid(screen, grid_size, start, goals, walls)

        # Cập nhật màn hình
        pygame.display.flip()

    # Thoát khỏi Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
