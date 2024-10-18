def dfs(grid_size, start, goals, walls):
    N, M = grid_size
    stack = [(start, [])]  # Stack chứa các trạng thái và đường đi
    visited = set()
    
    # Định nghĩa các bước di chuyển: lên, trái, xuống, phải
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    
    while stack:
        (current, path) = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Kiểm tra xem có đạt đích không
        if current in goals:
            return path

        # Thêm các trạng thái kề vào stack nếu chúng hợp lệ
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < N and 0 <= next_pos[1] < M and next_pos not in walls and next_pos not in visited:
                stack.append((next_pos, path))
    
    return None  # Không tìm thấy đường đi
from collections import deque

def bfs(grid_size, start, goals, walls):
    N, M = grid_size
    queue = deque([(start, [])])  # Queue chứa các trạng thái và đường đi
    visited = set()
    
    # Định nghĩa các bước di chuyển: lên, trái, xuống, phải
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    
    while queue:
        (current, path) = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Kiểm tra xem có đạt đích không
        if current in goals:
            return path

        # Thêm các trạng thái kề vào queue nếu chúng hợp lệ
        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if 0 <= next_pos[0] < N and 0 <= next_pos[1] < M and next_pos not in walls and next_pos not in visited:
                queue.append((next_pos, path))
    
    return None  # Không tìm thấy đường đi
def read_robotnav_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        grid_size = eval(lines[0].strip())  # [N, M]
        start = eval(lines[1].strip())  # (x, y)
        goals = [eval(coord) for coord in lines[2].strip().split(" | ")]  # Goal positions
        walls = set()  # Set for walls to check quickly
        
        # Đọc các tường và thêm vào danh sách
        for line in lines[3:]:
            x, y, w, h = eval(line.strip())
            for i in range(h):
                for j in range(w):
                    walls.add((x + i, y + j))
                    
        return grid_size, start, goals, walls

# Ví dụ sử dụng
filename = 'RobotNav-test.txt'  # Thay bằng đường dẫn đến file của bạn
grid_size, start, goals, walls = read_robotnav_file(filename)

# Chạy DFS
path_dfs = dfs(grid_size, start, goals, walls)
print("DFS Path:", path_dfs)

# Chạy BFS
path_bfs = bfs(grid_size, start, goals, walls)
print("BFS Path:", path_bfs)
