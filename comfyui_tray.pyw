"""ComfyUI 系统托盘程序"""
import subprocess
import sys
import os
import webbrowser
import threading
from PIL import Image, ImageDraw
import pystray

COMFYUI_DIR = os.path.dirname(os.path.abspath(__file__))
COMFYUI_URL = "http://127.0.0.1:8188"

process = None

def create_icon():
    """创建一个简单的图标"""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个渐变圆形
    draw.ellipse([4, 4, size-4, size-4], fill=(100, 149, 237))  # 蓝色
    draw.ellipse([16, 16, size-16, size-16], fill=(255, 255, 255))  # 白色中心
    return img

def start_comfyui():
    """启动 ComfyUI 服务"""
    global process
    if process and process.poll() is None:
        return

    python_exe = sys.executable.replace('pythonw.exe', 'python.exe')
    main_py = os.path.join(COMFYUI_DIR, 'main.py')

    # 启动参数（ROCm 7.2 原生支持，无需 --directml）
    args = [
        python_exe, main_py,
        '--use-pytorch-cross-attention', '--force-fp16',
        '--listen', '0.0.0.0', '--port', '8188'
    ]

    # 隐藏窗口启动
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    process = subprocess.Popen(
        args,
        cwd=COMFYUI_DIR,
        startupinfo=startupinfo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def stop_comfyui():
    """停止 ComfyUI 服务"""
    global process
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        process = None

def open_browser(icon, item):
    """打开浏览器"""
    webbrowser.open(COMFYUI_URL)

def restart_service(icon, item):
    """重启服务"""
    stop_comfyui()
    start_comfyui()

def quit_app(icon, item):
    """退出程序"""
    stop_comfyui()
    icon.stop()

def setup(icon):
    """托盘图标设置完成后启动服务"""
    icon.visible = True
    start_comfyui()

def main():
    icon = pystray.Icon(
        'ComfyUI',
        create_icon(),
        'ComfyUI Server',
        menu=pystray.Menu(
            pystray.MenuItem('打开 ComfyUI', open_browser, default=True),
            pystray.MenuItem('重启服务', restart_service),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('退出', quit_app)
        )
    )
    icon.run(setup)

if __name__ == '__main__':
    main()
