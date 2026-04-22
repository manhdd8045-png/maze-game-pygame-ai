# guard.py
import pygame
from astar import astar, bfs # Import cả 2 thuật toán

class Guard:
    def __init__(self, x, y, patrol_points, level="hard"):
        self.grid_pos = (x, y)
        self.patrol_points = patrol_points
        self.patrol_idx = 0
        self.level = level # "easy" (BFS) hoặc "hard" (A*)
        self.path = []
        self.speed_counter = 0

    def update(self, player_pos, grid_map):
        # Giảm tốc độ AI một chút để người chơi kịp chạy
        self.speed_counter += 1
        if self.speed_counter % 10 != 0: return 

        dist = distance(self.grid_pos, player_pos)
        
        # Nếu gần player trong 7 ô thì đuổi
        if dist < 7:
            if self.level == "hard":
                self.path = astar(grid_map, self.grid_pos, player_pos)
            else:
                self.path = bfs(grid_map, self.grid_pos, player_pos)
        else:
            # Đi tuần
            target = self.patrol_points[self.patrol_idx]
            self.path = astar(grid_map, self.grid_pos, target)
            if self.grid_pos == target:
                self.patrol_idx = (self.patrol_idx + 1) % len(self.patrol_points)

        if self.path and len(self.path) > 1:
            # path[0] thường là vị trí hiện tại, nên ta lấy path[1]
            self.grid_pos = self.path[1] 

    def draw(self, screen, tile_size):
        color = (255, 0, 0) if self.level == "hard" else (255, 165, 0)
        pygame.draw.rect(screen, color, (self.grid_pos[0]*tile_size, self.grid_pos[1]*tile_size, tile_size, tile_size))

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])