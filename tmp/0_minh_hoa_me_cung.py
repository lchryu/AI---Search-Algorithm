import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Hàm đọc dữ liệu từ file
def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    grid_size = eval(lines[0].strip())  # [rows, columns]
    start = eval(lines[1].strip())  # Vị trí bắt đầu
    goals = [eval(g.strip()) for g in lines[2].split('|')]  # Các vị trí đích
    walls = [eval(w.strip()) for w in lines[3:]]  # Các bức tường
    return grid_size, start, goals, walls


# Hàm vẽ lưới dựa trên dữ liệu đã đọc
def draw_grid(grid_size, start, goals, walls):
    rows, cols = grid_size
    fig, ax = plt.subplots(figsize=(10, 5))

    # Vẽ lưới
    for row in range(rows):
        for col in range(cols):
            rect = patches.Rectangle((col, row), 1, 1, edgecolor='black', facecolor='white')
            ax.add_patch(rect)

    # Vẽ tường với tọa độ (x, y), chiều rộng w, chiều cao h
    for wall in walls:
        x, y, w, h = wall
        rect = patches.Rectangle((y, x), w, h, edgecolor='black', facecolor='gray')  # Chú ý hoán đổi x và y
        ax.add_patch(rect)

    # Vẽ vị trí bắt đầu (robot)
    ax.add_patch(patches.Rectangle((start[1], start[0]), 1, 1, edgecolor='black', facecolor='red'))

    # Vẽ các vị trí đích (goals)
    for goal in goals:
        ax.add_patch(patches.Rectangle((goal[1], goal[0]), 1, 1, edgecolor='black', facecolor='green'))

    # Cài đặt trục
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.set_xticklabels(range(cols))
    ax.set_yticklabels(range(rows))
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()


# Đọc dữ liệu từ file và vẽ
filename = 'RobotNav-test.txt'  # Thay bằng đường dẫn đến file của bạn
grid_size, start, goals, walls = load_data(filename)
draw_grid(grid_size, start, goals, walls)
