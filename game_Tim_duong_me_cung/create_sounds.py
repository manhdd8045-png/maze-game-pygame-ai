import wave
import struct
import math

def generate_wav(filename, frequency, duration, volume=0.5, type="sine"):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # Mono
        f.setsampwidth(2) # 2 bytes per sample
        f.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            if type == "sine":
                val = math.sin(2 * math.pi * frequency * t)
            elif type == "square": # Tiếng bíp bíp 8-bit
                val = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            
            sample = int(val * volume * 32767)
            f.writeframesraw(struct.pack('<h', sample))
    print(f"✅ Đã tạo file: {filename}")

# --- TẠO CÁC FILE ÂM THANH ---
# 1. Nhạc nền (Trầm, hồi hộp)
generate_wav("background_music.wav", 110, 2.0, volume=0.3, type="sine")

# 2. Tiếng khi thắng (Cao, vui vẻ)
generate_wav("win.wav", 880, 0.5, type="square")

# 3. Tiếng khi bị bắt (Trầm, giật mình)
generate_wav("caught.wav", 60, 0.8, type="square")

# 4. Tiếng cảnh báo (Bíp bíp dồn dập)
generate_wav("warning.wav", 1200, 0.1, type="square")