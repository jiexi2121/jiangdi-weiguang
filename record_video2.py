"""用chrome headless + ffmpeg录制动态HTML"""
import subprocess
import os
import time
import shutil

temp_dir = "/tmp/video_frames2"
os.makedirs(temp_dir, exist_ok=True)

# 每页截图多帧
pages = [
    {"url": "http://localhost:8000/slides_A/slide1.html", "duration": 6},
    {"url": "http://localhost:8000/slides_A/slide2.html", "duration": 6},
    {"url": "http://localhost:8000/slides_A/slide3.html", "duration": 6},
    {"url": "http://localhost:8000/slides_A/slide4.html", "duration": 6},
]

fps = 8
total = 0

for page_idx, pg in enumerate(pages):
    frames = pg["duration"] * fps
    for f in range(frames):
        out = os.path.join(temp_dir, f"frame_{total:06d}.png")
        # 用chrome截图
        subprocess.run([
            "google-chrome", "--headless", "--disable-gpu",
            "--screenshot=" + out,
            "--window-size=1920,1080",
            "--no-sandbox",
            "--virtual-time-budget=3000",
            pg["url"]
        ], capture_output=True, timeout=15)
        total += 1
        if f % 5 == 0:
            print(f"  page {page_idx+1} frame {f}/{frames}")

print(f"总共 {total} 帧")

# ffmpeg合成
output = "/workspace/江底微光_动态循环.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", f"{temp_dir}/frame_%06d.png",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "23",
    "-preset", "fast",
    "-movflags", "+faststart",
    output
], check=True)
print(f"视频已生成: {output}")
shutil.rmtree(temp_dir)
