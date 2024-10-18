import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Hàm vẽ lưới điều hướng robot từng bước
def draw_grid_step(
    ax, grid_size, start, goals, walls, current=None, path=None, visited=None
):
    ax.clear()  # Xóa nội dung cũ
    N, M = grid_size
    ax.set_xlim(0, M)
    ax.set_ylim(0, N)

    # Vẽ các tường
    for wall in walls:
        x, y = wall
        rect = patches.Rectangle(
            (y, x), 1, 1, linewidth=1, edgecolor="black", facecolor="gray"
        )
        ax.add_patch(rect)

    # Vẽ vị trí bắt đầu
    ax.plot(start[1], start[0], "ro", label="Start (Robot)", markersize=15)

    # Vẽ các vị trí đích
    for goal in goals:
        ax.plot(
            goal[1],
            goal[0],
            "go",
            label="Goal",
            markersize=15,
            markerfacecolor="green",
            markeredgewidth=2,
            markeredgecolor="black",
        )

    # Vẽ đường đi (nếu có)
    if path:
        for i in range(len(path) - 1):
            ax.plot(
                [path[i][1], path[i + 1][1]],
                [path[i][0], path[i + 1][0]],
                "b-",
                linewidth=2,
            )

    # Vẽ các ô đã duyệt qua (visited)
    if visited:
        for node in visited:
            ax.plot(node[1], node[0], "yo", markersize=8)  # Đánh dấu ô đã thăm

    # Vẽ ô hiện tại (nếu có)
    if current:
        ax.plot(current[1], current[0], "co", markersize=12, label="Current")

    # Hiển thị lưới
    ax.set_xticks(range(M))
    ax.set_yticks(range(N))
    ax.set_xticklabels(range(M))
    ax.set_yticklabels(range(N))
    ax.grid(True)
    plt.gca().invert_yaxis()
    plt.draw()
    plt.pause(0.5)  # Tạm dừng 0.5 giây để xem từng bước


# Hàm xử lý sự kiện khi nhấn nút "Run"
def run_search():
    method = search_method.get()  # Lấy phương pháp tìm kiếm được chọn
    if method not in ["DFS", "BFS"]:
        messagebox.showerror("Error", "Please select a valid search method")
        return

    # Đọc dữ liệu từ file và chạy thuật toán tương ứng
    grid_size, start, goals, walls = read_robotnav_file("RobotNav-test.txt")

    fig, ax = plt.subplots(figsize=(12, 6))  # Tạo cửa sổ vẽ duy nhất
    plt.ion()  # Bật chế độ tương tác của matplotlib

    if method == "DFS":
        path = dfs(grid_size, start, goals, walls, ax)
    elif method == "BFS":
        path = bfs(grid_size, start, goals, walls, ax)

    plt.ioff()  # Tắt chế độ tương tác sau khi hoàn thành
    if path:
        draw_grid_step(ax, grid_size, start, goals, walls, path=path)
    else:
        messagebox.showinfo("No Solution", "No path to the goal could be found!")


# Hàm đọc file RobotNav-test.txt
def read_robotnav_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        grid_size = eval(lines[0].strip())  # [N, M]
        start = eval(lines[1].strip())  # (x, y)
        goals = [
            eval(coord) for coord in lines[2].strip().split(" | ")
        ]  # Goal positions
        walls = set()  # Set for walls to check quickly

        # Đọc các tường và thêm từng tọa độ ô tường vào danh sách
        for line in lines[3:]:
            x, y, w, h = eval(line.strip())  # Tường được mô tả bởi (x, y, w, h)
            for i in range(h):
                for j in range(w):
                    walls.add((x + i, y + j))  # Thêm từng ô của tường vào danh sách

        return grid_size, start, goals, walls


# Cài đặt giải thuật tìm kiếm DFS với từng bước
def dfs(grid_size, start, goals, walls, ax):
    N, M = grid_size
    stack = [(start, [])]  # Stack chứa các trạng thái và đường đi
    visited = set()

    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while stack:
        (current, path) = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Vẽ mỗi bước
        draw_grid_step(
            ax,
            grid_size,
            start,
            goals,
            walls,
            current=current,
            path=path,
            visited=visited,
        )

        if current in goals:
            return path

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if (
                0 <= next_pos[0] < N
                and 0 <= next_pos[1] < M
                and next_pos not in walls
                and next_pos not in visited
            ):
                stack.append((next_pos, path))

    return None


# Cài đặt giải thuật tìm kiếm BFS với từng bước
def bfs(grid_size, start, goals, walls, ax):
    from collections import deque

    N, M = grid_size
    queue = deque([(start, [])])
    visited = set()

    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while queue:
        (current, path) = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        # Vẽ mỗi bước
        draw_grid_step(
            ax,
            grid_size,
            start,
            goals,
            walls,
            current=current,
            path=path,
            visited=visited,
        )

        if current in goals:
            return path

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if (
                0 <= next_pos[0] < N
                and 0 <= next_pos[1] < M
                and next_pos not in walls
                and next_pos not in visited
            ):
                queue.append((next_pos, path))

    return None


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Robot Navigation")

# Label và combobox để chọn phương pháp tìm kiếm
tk.Label(root, text="Select Search Method:").pack(pady=10)
search_method = tk.StringVar()
method_menu = tk.OptionMenu(root, search_method, "DFS", "BFS")
method_menu.pack()

# Nút chạy thuật toán
run_button = tk.Button(root, text="Run", command=run_search)
run_button.pack(pady=20)

# Chạy giao diện chính
root.mainloop()
