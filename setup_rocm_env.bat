@echo off
REM ComfyUI ROCm 7.2 环境一键安装脚本
REM 前置条件：Miniconda 已安装，AMD ROCm 专用驱动 26.1.1+ 已安装

echo === ComfyUI ROCm 7.2 环境安装 ===

REM 1. 创建 Python 3.12 环境
echo [1/5] 创建 Conda 环境...
call conda create -n ComfyUI_ROCm python=3.12 -y
call conda activate ComfyUI_ROCm

REM 2. 安装 ROCm 7.2 SDK
echo [2/5] 安装 ROCm 7.2 SDK（约 2.5 GB）...
pip install --no-cache-dir ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz

REM 3. 安装 PyTorch ROCm 版
echo [3/5] 安装 PyTorch 2.9.1 ROCm（约 820 MB）...
pip install --no-cache-dir ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%%2Brocmsdk20260116-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchaudio-2.9.1%%2Brocmsdk20260116-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1%%2Brocmsdk20260116-cp312-cp312-win_amd64.whl

REM 4. 安装 ComfyUI 依赖
echo [4/5] 安装 ComfyUI 依赖...
pip install -r requirements.txt
pip install -r manager_requirements.txt
pip install pystray pillow

REM 5. 验证
echo [5/5] 验证 GPU 识别...
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0)); print('VRAM:', round(torch.cuda.get_device_properties(0).total_memory/1024**3), 'GB')"

echo.
echo === 安装完成！运行 Start_ComfyUI_Tray.bat 启动 ===
pause
