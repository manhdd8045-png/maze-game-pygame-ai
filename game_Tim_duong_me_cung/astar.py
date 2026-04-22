# astar.py
import heapq
from collections import deque

def get_neighbors(pos, grid_map):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(grid_map[0]) and 0 <= ny < len(grid_map):
            if grid_map[ny][nx] == 0: # Đường đi được
                neighbors.append((nx, ny))
    return neighbors

# Đổi tên thành 'astar' để không còn lỗi ImportError
def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from and current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            new_g = g_score[current] + 1
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f_score = new_g + abs(neighbor[0]-goal[0]) + abs(neighbor[1]-goal[1])
                heapq.heappush(open_set, (f_score, neighbor))
                came_from[neighbor] = current
    return []

# Thêm hàm BFS cho AI cấp độ dễ
def bfs(grid, start, goal):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
    return []