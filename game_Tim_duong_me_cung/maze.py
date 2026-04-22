import random

def generate_maze(rows, cols):
    # đảm bảo kích thước lẻ để maze đẹp hơn
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    # 1 = tường, 0 = đường đi
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve(x, y):
        directions = [(0,2), (2,0), (0,-2), (-2,0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # kiểm tra hợp lệ
            if 1 <= nx < cols-1 and 1 <= ny < rows-1:
                if maze[ny][nx] == 1:
                    # phá tường giữa
                    maze[ny][nx] = 0
                    maze[y + dy//2][x + dx//2] = 0

                    carve(nx, ny)

    # điểm bắt đầu
    maze[1][1] = 0
    carve(1, 1)

    return maze