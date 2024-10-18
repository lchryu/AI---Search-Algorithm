class Grid:
    def __init__(self, n, m, walls):
        self.grid = [[0 for _ in range(m)] for _ in range(n)]  # Tạo lưới NxM
        for wall in walls:
            x, y, w, h = wall
            # Kiểm tra xem tường có nằm trong giới hạn của lưới không
            if x < 0 or y < 0 or x + h > n or y + w > m:
                raise ValueError(
                    f"Tường ({x}, {y}, {w}, {h}) nằm ngoài giới hạn của lưới {n}x{m}"
                )

            # Đánh dấu các ô chứa tường
            for i in range(h):
                for j in range(w):
                    if (
                        0 <= x + i < n and 0 <= y + j < m
                    ):  # Chỉ đánh dấu nếu trong giới hạn
                        self.grid[x + i][y + j] = 1


def get_neighbors(grid, current):
    n, m = len(grid.grid), len(grid.grid[0])  # Kích thước lưới
    x, y = current  # Vị trí hiện tại của robot
    neighbors = []

    # Di chuyển lên (UP)
    if x > 0 and grid.grid[x - 1][y] == 0:
        neighbors.append((x - 1, y))

    # Di chuyển trái (LEFT)
    if y > 0 and grid.grid[x][y - 1] == 0:
        neighbors.append((x, y - 1))

    # Di chuyển xuống (DOWN)
    if x < n - 1 and grid.grid[x + 1][y] == 0:
        neighbors.append((x + 1, y))

    # Di chuyển phải (RIGHT)
    if y < m - 1 and grid.grid[x][y + 1] == 0:
        neighbors.append((x, y + 1))

    return neighbors


def dfs(grid, start, goals):
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        print(f"Đang kiểm tra: {current}")  # Hiển thị ô hiện tại
        if current in goals:
            print(f"Đã tìm thấy mục tiêu tại {current}")
            return current
        visited.add(current)
        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                stack.append(neighbor)
    print("Không tìm thấy đường đi đến mục tiêu")
    return None  # Không tìm thấy đường đi


def load_data(filename):
    """Hàm đọc dữ liệu từ tệp và khởi tạo lưới, vị trí robot và mục tiêu"""
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Đọc kích thước lưới
    grid_size = eval(lines[0].strip())  # [N, M]
    n, m = grid_size
    
    # Đọc vị trí bắt đầu của robot
    start = eval(lines[1].strip())  # (x1, y1)
    
    # Đọc các vị trí đích
    goals = [eval(goal.strip()) for goal in lines[2].split('|')]  # (xg1, yg1) | (xg2, yg2) ...
    
    # Đọc các bức tường
    walls = [eval(wall.strip()) for wall in lines[3:] if eval(wall.strip())[0] < n]  # Chỉ giữ tường trong giới hạn
    
    return n, m, start, goals, walls



def main():
    # Load dữ liệu từ tệp
    filename = "RobotNav-test.txt"  # Đường dẫn tệp
    n, m, start, goals, walls = load_data(filename)

    # Khởi tạo lưới
    grid = Grid(n, m, walls)

    # Chạy DFS
    print("Kết quả DFS:")
    result = dfs(grid, start, goals)
    print(f"Kết quả cuối cùng: {result}")
# ---------------------------------------------------------------
import heapq

# Hàm tính khoảng cách Manhattan (hàm heuristic)
def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# Greedy Best-First Search (GBFS)
def gbfs(grid_size, start, goals, walls, ax):
    N, M = grid_size
    queue = []
    visited = set()

    # Thêm trạng thái ban đầu vào hàng đợi ưu tiên với chi phí heuristic
    for goal in goals:
        heapq.heappush(queue, (manhattan_distance(start, goal), start, []))  # (cost, current, path)

    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    
    while queue:
        _, current, path = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Vẽ mỗi bước
        draw_grid_step(ax, grid_size, start, goals, walls, current=current, path=path, visited=visited)

        if current in goals:
            return path

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < N and 0 <= next_pos[1] < M and next_pos not in walls and next_pos not in visited:
                # Ước tính chi phí đến mục tiêu bằng khoảng cách heuristic (Manhattan)
                for goal in goals:
                    cost = manhattan_distance(next_pos, goal)
                    heapq.heappush(queue, (cost, next_pos, path))
    
    return None

# A-star Search (A*)
def a_star(grid_size, start, goals, walls, ax):
    N, M = grid_size
    queue = []
    visited = set()
    g_cost = {start: 0}  # Chi phí từ trạng thái bắt đầu đến mỗi trạng thái

    # Thêm trạng thái ban đầu vào hàng đợi ưu tiên với tổng chi phí g(n) + h(n)
    for goal in goals:
        heapq.heappush(queue, (g_cost[start] + manhattan_distance(start, goal), start, []))  # (total_cost, current, path)

    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    
    while queue:
        _, current, path = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Vẽ mỗi bước
        draw_grid_step(ax, grid_size, start, goals, walls, current=current, path=path, visited=visited)

        if current in goals:
            return path

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < N and 0 <= next_pos[1] < M and next_pos not in walls and next_pos not in visited:
                new_g_cost = g_cost[current] + 1  # Mỗi bước có chi phí 1
                if next_pos not in g_cost or new_g_cost < g_cost[next_pos]:
                    g_cost[next_pos] = new_g_cost
                    for goal in goals:
                        f_cost = new_g_cost + manhattan_distance(next_pos, goal)
                        heapq.heappush(queue, (f_cost, next_pos, path))
    
    return None

def run_search():
    method = search_method.get()  # Lấy phương pháp tìm kiếm được chọn
    if method not in ["DFS", "BFS", "GBFS", "A*"]:
        messagebox.showerror("Error", "Please select a valid search method")
        return

    # Đọc dữ liệu từ file và chạy thuật toán tương ứng
    grid_size, start, goals, walls = read_robotnav_file('RobotNav-test.txt')
    
    fig, ax = plt.subplots(figsize=(12, 6))  # Tạo cửa sổ vẽ duy nhất
    plt.ion()  # Bật chế độ tương tác của matplotlib

    if method == "DFS":
        path = dfs(grid_size, start, goals, walls, ax)
    elif method == "BFS":
        path = bfs(grid_size, start, goals, walls, ax)
    elif method == "GBFS":
        path = gbfs(grid_size, start, goals, walls, ax)
    elif method == "A*":
        path = a_star(grid_size, start, goals, walls, ax)

    plt.ioff()  # Tắt chế độ tương tác sau khi hoàn thành
    if path:
        draw_grid_step(ax, grid_size, start, goals, walls, path=path)
    else:
        messagebox.showinfo("No Solution", "No path to the goal could be found!")


if __name__ == "__main__":
    main()
