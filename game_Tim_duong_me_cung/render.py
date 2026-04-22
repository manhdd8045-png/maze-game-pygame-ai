import pygame
from config import *

def draw(screen, grid, player, guards, goal, warning):
    # Vẽ bản đồ (Gỗ, Cỏ, Safe Zone)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 1:
                color = (139, 69, 19)   # gỗ
            elif val == 0:
                color = (34, 139, 34)   # cỏ
            else:
                color = (200, 230, 255) # safe

            pygame.draw.rect(screen, color,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Vẽ Player (Hình tròn màu xanh)
    px, py = player.pos
    pygame.draw.circle(screen, (0, 0, 255),
        (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Vẽ Guard (Quái vật)
    for g in guards:
        # SỬA LỖI Ở ĐÂY: g.pos -> g.grid_pos
        gx, gy = g.grid_pos 
        
        # Màu sắc theo cấp độ: Hard = Đỏ tươi, Easy = Cam
        g_color = (255, 0, 0) if g.level == "hard" else (255, 165, 0)
        
        pygame.draw.rect(screen, g_color,
            (gx * CELL_SIZE + 5, gy * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

    # Vẽ Goal 💎 (Hình thoi vàng)
    goal_x, goal_y = goal
    pygame.draw.polygon(screen, (255, 215, 0), [
        (goal_x * CELL_SIZE + CELL_SIZE // 2, goal_y * CELL_SIZE + 5),
        (goal_x * CELL_SIZE + CELL_SIZE - 5, goal_y * CELL_SIZE + CELL_SIZE // 2),
        (goal_x * CELL_SIZE + CELL_SIZE // 2, goal_y * CELL_SIZE + CELL_SIZE - 5),
        (goal_x * CELL_SIZE + 5, goal_y * CELL_SIZE + CELL_SIZE // 2)
    ])

    # ⚠️ Cảnh báo đỏ khi sắp hết thời gian an toàn
    if warning:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(80)
        overlay.fill((255, 0, 0))
        screen.blit(overlay, (0, 0))