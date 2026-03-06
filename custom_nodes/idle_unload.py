"""闲时自动释放模型和显存

通过后台线程监控队列状态，当空闲超过指定时间后自动卸载所有模型并清理显存。
通过环境变量 COMFYUI_IDLE_TIMEOUT 配置超时秒数，默认 300 秒（5 分钟）。
设为 0 则禁用此功能。
"""
import os
import time
import gc
import logging
import threading
import comfy.model_management
from server import PromptServer

IdleTimeout = float(os.environ.get("COMFYUI_IDLE_TIMEOUT", "300"))

def IdleWatchdog():
    """后台监控线程：检测空闲并释放显存"""
    Server = PromptServer.instance
    LastBusyTime = time.time()
    Unloaded = False

    while True:
        time.sleep(10)
        TasksRemaining = Server.prompt_queue.get_tasks_remaining()

        if TasksRemaining > 0:
            # 队列有任务，重置计时
            LastBusyTime = time.time()
            Unloaded = False
            continue

        if Unloaded:
            continue

        IdleSeconds = time.time() - LastBusyTime
        if IdleSeconds >= IdleTimeout:
            logging.info("闲置超过 {:.0f} 秒，自动释放模型和显存".format(IdleTimeout))
            # 通过队列标记触发释放（与 ComfyUI 内部机制一致）
            Server.prompt_queue.set_flag("unload_models", True)
            Server.prompt_queue.set_flag("free_memory", True)
            # 额外清理 Python 垃圾和 GPU 缓存
            gc.collect()
            comfy.model_management.soft_empty_cache()
            Unloaded = True
            logging.info("模型已释放，显存已清理")

if IdleTimeout > 0:
    T = threading.Thread(target=IdleWatchdog, daemon=True)
    T.start()
    logging.info("闲时自动释放已启用，超时: {:.0f} 秒".format(IdleTimeout))
else:
    logging.info("闲时自动释放已禁用（COMFYUI_IDLE_TIMEOUT=0）")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
