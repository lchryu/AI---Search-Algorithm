import sys
from collections import deque
import pygame


def read_file(filename):
    """
    Đọc dữ liệu từ file.
    """
    with open(filename, "r") as f:
        lines = f.readlines()
        grid_size = tuple(map(int, lines[0].strip()[1:-1].split(",")))
        start = tuple(map(int, lines[1].strip()[1:-1].split(",")))
        goals = [
            tuple(map(int, goal.strip()[1:-1].split(",")))
            for goal in lines[2].strip().split("|")
        ]
        walls = set()
        for line in lines[3:]:
            x, y, w, h = map(int, line.strip()[1:-1].split(","))
            for i in range(x, x + w):
                for j in range(y, y + h):
                    walls.add((i, j))
        return grid_size, start, goals, walls


def create_grid(grid_size, walls):
    """
    Tạo ma trận biểu diễn lưới.
    """
    grid = [["." for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    for x, y in walls:
        if 0 <= x < grid_size[0] and 0 <= y < grid_size[1]:
            grid[x][y] = "#"
    return grid


def bfs(grid, start, goals, walls):
    """
    Thực hiện thuật toán tìm kiếm theo chiều rộng (BFS).
    """
    queue = deque([(start, [], 0)])
    visited = set([start])

    while queue:
        (x, y), path, nodes_created = queue.popleft()

        if (x, y) in goals:
            return (x, y), nodes_created + 1, path

        for dx, dy, move in [
            (0, -1, "up"),
            (-1, 0, "left"),
            (0, 1, "down"),
            (1, 0, "right"),
        ]:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid[0])
                and (new_x, new_y) not in walls
                and (new_x, new_y) not in visited
            ):
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [move], nodes_created + 1))

    return None, nodes_created, None


import sys
from collections import deque
import pygame

# ... (Các hàm read_file, create_grid, bfs giữ nguyên)


def visualize_path(grid, start, goal, path, walls):
    """
    Hiển thị đường đi bằng Pygame.
    """
    pygame.init()

    cell_size = 50
    grid_width, grid_height = len(grid[0]), len(grid)
    screen_width = grid_width * cell_size
    screen_height = grid_height * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Robot Navigation")

    colors = {
        ".": (255, 255, 255),  # Màu trắng cho ô trống
        "#": (0, 0, 0),  # Màu đen cho tường
        "S": (0, 255, 0),  # Màu xanh lá cây cho điểm bắt đầu
        "G": (255, 0, 0),  # Màu đỏ cho điểm đích
        "P": (0, 0, 255),  # Màu xanh dương cho đường đi
        "V": (200, 200, 200),  # Màu xám cho nút đã thăm
    }

    visited = set()  # Lưu trữ các nút đã thăm

    running = True
    current_x, current_y = start
    for move in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Vẽ lưới
        for i in range(grid_height):
            for j in range(grid_width):
                color = colors[grid[i][j]]
                if (i, j) in visited:
                    color = colors["V"]  # Tô màu xám cho nút đã thăm
                pygame.draw.rect(
                    screen, color, (j * cell_size, i * cell_size, cell_size, cell_size)
                )

        # Vẽ điểm bắt đầu và điểm đích
        pygame.draw.circle(
            screen,
            colors["S"],
            (
                start[1] * cell_size + cell_size // 2,
                start[0] * cell_size + cell_size // 2,
            ),
            cell_size // 3,
        )
        pygame.draw.circle(
            screen,
            colors["G"],
            (
                goal[1] * cell_size + cell_size // 2,
                goal[0] * cell_size + cell_size // 2,
            ),
            cell_size // 3,
        )

        # Vẽ đường đi
        if move == "up":
            current_x -= 1
        elif move == "down":
            current_x += 1
        elif move == "left":
            current_y -= 1
        elif move == "right":
            current_y += 1
        visited.add((current_x, current_y))  # Đánh dấu nút hiện tại là đã thăm

        pygame.draw.circle(
            screen,
            colors["P"],
            (
                current_y * cell_size + cell_size // 2,
                current_x * cell_size + cell_size // 2,
            ),
            cell_size // 3,
        )
        pygame.display.flip()
        pygame.time.delay(500)

    # Giữ cửa sổ hiển thị đến khi người dùng đóng
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# ... (Hàm main giữ nguyên)
def main():
    """
    Hàm main để chạy chương trình.
    """
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    grid_size, start, goals, walls = read_file(filename)
    grid = create_grid(grid_size, walls)

    if method == "BFS":
        goal, nodes_created, path = bfs(grid, start, goals, walls)
    # ... (Các phương thức khác)

    if goal:
        print(f"{filename} {method}")
        print(f"{goal[0]},{goal[1]} {nodes_created}")
        print("; ".join(path))

        # Hiển thị đường đi bằng Pygame
        visualize_path(grid, start, goal, path, walls)
    else:
        print(f"{filename} {method}")
        print(f"No goal is reachable; {nodes_created}")


if __name__ == "__main__":
    main()
