"""录制动态HTML幻灯片为MP4视频"""
import subprocess
import os
import time

# 方案：用chrome headless + screencast 或直接用ffmpeg录Xvfb
# 最简单可靠：用playwright录制 + ffmpeg编码

from playwright.sync_api import sync_playwright

# 启动HTTP服务器
import http.server
import threading
import socketserver

PORT = 8765
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
thread = threading.Thread(target=httpd.serve_forever, daemon=True)
thread.start()
time.sleep(1)

URL = f"http://localhost:{PORT}/江底微光_版本A.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 创建上下文，viewport设置为16:9
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
    )
    
    page = context.new_page()
    page.goto(URL, wait_until="networkidle")
    time.sleep(3)  # 等动画启动
    
    # 录制视频 - 使用playwright内置录制
    # 先截取4帧确认能正常渲染
    slides_info = [
        {"name": "slide1", "selector": "#slide1", "duration": 7},
        {"name": "slide2", "selector": "#slide2", "duration": 7},
        {"name": "slide3", "selector": "#slide3", "duration": 7},
        {"name": "slide4", "selector": "#slide4", "duration": 7},
    ]
    
    # Playwright没有内置录屏到文件的功能
    # 改用逐帧截图 + ffmpeg合成
    
    temp_dir = "/tmp/video_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    fps = 10  # 10帧每秒足够，减小文件大小
    total_frames = 0
    
    for slide_info in slides_info:
        # 滚动到该幻灯片
        slide_el = page.query_selector(slide_info["selector"])
        if slide_el:
            slide_el.scroll_into_view_if_needed()
        time.sleep(1)  # 等动画稳定
        
        frames_needed = slide_info["duration"] * fps
        for f in range(frames_needed):
            frame_path = os.path.join(temp_dir, f"frame_{total_frames:06d}.png")
            page.screenshot(path=frame_path, full_page=False)
            total_frames += 1
            time.sleep(1.0 / fps)
    
    browser.close()

httpd.shutdown()

print(f"总共 {total_frames} 帧已保存到 {temp_dir}")

# 用ffmpeg合成视频
output_video = "/workspace/江底微光_动态循环.mp4"
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", f"{temp_dir}/frame_%06d.png",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "23",
    "-preset", "fast",
    output_video
]
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stderr[-500:] if result.stderr else "ffmpeg OK")
print(f"视频已生成: {output_video}")
