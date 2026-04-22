import pygame
import time


class Player:
    def __init__(self, x, y):
        self.pos = (x, y)
        
        # --- QUẢN LÝ TỐC ĐỘ ---
        # 0.8 tốc độ nghĩa là chúng ta cần một khoảng trễ khi nhấn phím
        self.move_delay = 0.15  # Thời gian chờ giữa các bước đi (giây)
        self.last_move_time = 0
        
        # --- TIMER SAFE ZONE ---
        self.safe_start = None

    # 🎮 di chuyển (Đã thêm kiểm tra tốc độ)
    def move(self, dx, dy, grid):
        current_time = time.time()
        
        # Chỉ cho phép di chuyển nếu đã qua khoảng thời gian delay
        if current_time - self.last_move_time < self.move_delay:
            return False

        x, y = self.pos
        nx, ny = x + dx, y + dy

        # kiểm tra không ra ngoài map + không đi vào tường
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != 1:  # 1 = tường
                self.pos = (nx, ny)
                self.last_move_time = current_time # Cập nhật thời gian di chuyển cuối
                return True
        return False

    # 🟩 kiểm tra đang ở safe zone
    def in_safe_zone(self, grid):
        x, y = self.pos
        # Tránh lỗi index out of range nếu cần
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            return grid[y][x] == 2   # 2 = safe zone
        return False

    # ⏱ cập nhật thời gian đứng trong safe zone
    def update_safe_timer(self, grid):
        if self.in_safe_zone(grid):
            if self.safe_start is None:
                self.safe_start = time.time()
        else:
            # ra khỏi vùng an toàn → reset
            self.safe_start = None

    # ⌛ lấy thời gian đã đứng trong safe zone
    def safe_time(self):
        if self.safe_start is not None:
            return time.time() - self.safe_start
        return 0

    # ⚠️ kiểm tra cảnh báo (5s cuối)
    def is_warning(self):
        return 25 <= self.safe_time() < 30

    # 💀 kiểm tra chết do trap
    def is_dead_by_trap(self):
        return self.safe_time() >= 30
    
   