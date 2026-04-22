# map.py
import random
from astar import astar # Giờ đã chạy ok

SAFE = 2

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_grid_zone(x, y, cols, rows):
    zx = min(2, x // (cols // 3))
    zy = min(2, y // (rows // 3))
    return zx + zy * 3 

def add_safe_zones(grid, player_pos, goal):
    rows, cols = len(grid), len(grid[0])
    safe_positions = []

    # 🟩 SAFE 1: Gần player
    found = False
    for _ in range(50):
        nx = player_pos[0] + random.randint(-4, 4)
        ny = player_pos[1] + random.randint(-4, 4)
        if 1 <= nx < cols-1 and 1 <= ny < rows-1 and grid[ny][nx] == 0:
            grid[ny][nx] = SAFE
            safe_positions.append((nx, ny))
            found = True
            break

    # 🟩 SAFE 2: Trên đường đi A*
    path = astar(grid, player_pos, goal)
    if path and len(path) > 10:
        mid = path[len(path)//2]
        if grid[mid[1]][mid[0]] == 0:
            grid[mid[1]][mid[0]] = SAFE
            safe_positions.append(mid)

    # 🟩 SAFE 3: Vùng khác biệt
    attempts = 0
    while len(safe_positions) < 3 and attempts < 100:
        attempts += 1
        rx, ry = random.randint(1, cols-2), random.randint(1, rows-2)
        if grid[ry][rx] == 0:
            used_zones = [get_grid_zone(p[0], p[1], cols, rows) for p in safe_positions]
            if get_grid_zone(rx, ry, cols, rows) not in used_zones:
                if all(distance((rx, ry), p) >= 15 for p in safe_positions):
                    grid[ry][rx] = SAFE
                    safe_positions.append((rx, ry))
                    
    return safe_positions