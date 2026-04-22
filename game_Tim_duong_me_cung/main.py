import pygame
import sys
from config import *
from maze import generate_maze
from map import add_safe_zones
from player import Player
from guard import Guard
from render import draw

def main():
    # --- KHỞI TẠO HỆ THỐNG ---
    pygame.init()
    # Tăng buffer âm thanh để tránh lag
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze AI: Stealth Mission")
    clock = pygame.time.Clock()

    # --- KHỞI TẠO ÂM THANH ---
    sounds = {}
    try:
        # SỬA LỖI: Đổi .mp3 thành .wav vì file thực tế là .wav
        pygame.mixer.music.load("background_music.wav") 
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        sounds['caught'] = pygame.mixer.Sound("caught.wav")
        sounds['win'] = pygame.mixer.Sound("win.wav")
        sounds['warning'] = pygame.mixer.Sound("warning.wav")
        print("✅ Âm thanh đã sẵn sàng!")
    except Exception as e:
        print(f"⚠️ Không thể tải âm thanh: {e}")

    # --- KHỞI TẠO ĐỐI TƯỢNG GAME ---
    grid = generate_maze(ROWS, COLS)
    player = Player(1, 1)
    goal = (COLS - 2, ROWS - 2)

    # Thêm vùng an toàn
    add_safe_zones(grid, player.pos, goal)

    # SỬA LỖI: Đảm bảo truyền đủ tham số patrol_points cho Guard
    guards = [
        Guard(COLS-2, ROWS-2, [(COLS-2, ROWS-2), (COLS-6, ROWS-2)], level="hard"),
        Guard(COLS-2, 1, [(COLS-2, 1), (COLS-2, 6)], level="easy")
    ]

    running = True
    warning_played = False 

    # --- VÒNG LẶP GAME ---
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Xử lý di chuyển
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: player.move(0, -1, grid)
        if keys[pygame.K_DOWN]: player.move(0, 1, grid)
        if keys[pygame.K_LEFT]: player.move(-1, 0, grid)
        if keys[pygame.K_RIGHT]: player.move(1, 0, grid)

        # Cập nhật Logic
        player.update_safe_timer(grid)
        safe_time = player.safe_time()
        warning = 25 <= safe_time < 30

        # Âm thanh cảnh báo
        if warning and not warning_played:
            if 'warning' in sounds: sounds['warning'].play()
            warning_played = True
        elif not warning:
            warning_played = False

        # Kiểm tra thua cuộc do hết thời gian (Trap)
        if safe_time >= 30:
            pygame.mixer.music.stop()
            if 'caught' in sounds: sounds['caught'].play()
            print("💀 GAME OVER - TRAP")
            pygame.time.delay(1500)
            running = False

        # Cập nhật Guard và va chạm
        for g in guards:
            g.update(player.pos, grid) 

            # SỬA LỖI: Sử dụng g.grid_pos thay vì g.pos
            if g.grid_pos == player.pos:
                pygame.mixer.music.stop()
                if 'caught' in sounds: sounds['caught'].play()
                print("💀 GAME OVER - CAUGHT BY GUARD")
                pygame.time.delay(1500)
                running = False

        # Kiểm tra chiến thắng
        if player.pos == goal:
            pygame.mixer.music.stop()
            if 'win' in sounds: sounds['win'].play()
            print("🎉 YOU WIN!")
            pygame.time.delay(2000)
            running = False

        # Vẽ màn hình
        draw(screen, grid, player, guards, goal, warning)

        pygame.display.flip()
        clock.tick(15) # Tốc độ nhân vật sẽ chậm lại đáng kể ở mức 15 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()