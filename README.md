# ComfyUI

基于节点的 Stable Diffusion 可视化工作流编辑器。

本仓库 fork 自 [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)，添加了 ROCm 7.2 支持、托盘启动、闲时自动释放显存等功能。

## 环境配置

### 前置条件

- Windows 10/11
- Python 3.12（Miniconda）
- AMD Radeon RX 7000/9000 系列显卡
- [AMD ROCm PyTorch 专用驱动 26.1.1+](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-1-1.html)

### 安装步骤

1. **创建 Conda 环境**

```bash
conda create -n ComfyUI_ROCm python=3.12 -y
conda activate ComfyUI_ROCm
```

2. **安装 ROCm 7.2 SDK**

```bash
pip install --no-cache-dir ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz
```

3. **安装 PyTorch（ROCm 7.2）**

```bash
pip install --no-cache-dir ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchaudio-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl
```

4. **安装 ComfyUI 依赖**

```bash
pip install -r requirements.txt
pip install -r manager_requirements.txt
pip install -r requirements_extra.txt
```

5. **验证 GPU 识别**

```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
# 预期输出: AMD Radeon RX 7900 XTX
```

## 启动方式

### 托盘启动（推荐）

运行 `Start_ComfyUI_Tray.bat`，程序将在后台运行，任务栏显示托盘图标。已内置单实例锁，重复启动会自动忽略。

- **双击图标**：打开浏览器访问 ComfyUI
- **右键菜单**：打开 ComfyUI / 重启服务 / 退出

### 闲时自动释放显存

内置 `idle_unload` 插件，空闲 5 分钟后自动卸载模型并释放显存。通过环境变量 `COMFYUI_IDLE_TIMEOUT` 配置超时秒数（默认 300，设为 0 禁用）。

### 命令行启动

```bash
conda activate ComfyUI_ROCm
python main.py --use-pytorch-cross-attention --force-fp16 --listen 0.0.0.0 --port 8188
```

### 启动参数说明

| 参数 | 说明 |
|------|------|
| `--use-pytorch-cross-attention` | 使用 PyTorch 原生注意力（AMD ROCm 推荐） |
| `--force-fp16` | 强制 FP16 精度，节省显存 |
| `--listen 0.0.0.0` | 允许局域网访问 |
| `--port 8188` | 服务端口 |
| `--lowvram` | 低显存模式（可选） |

## 开机自启动

将 `Start_ComfyUI_Tray.bat` 的快捷方式放到：

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

## 快速恢复环境

已导出 `environment.yml`，可在新机器上一键恢复：

```bash
conda env create -f environment.yml
```

## 模型目录

| 类型 | 目录 |
|------|------|
| Checkpoint | `models/checkpoints` |
| VAE | `models/vae` |
| LoRA | `models/loras` |
| ControlNet | `models/controlnet` |
| Embeddings | `models/embeddings` |

## 已知限制

- RX 7900 XTX 不支持 FP8，可使用 BF16/FP16/INT8
- ROCm 7.2 Windows 版仅支持推理，训练需使用 Linux

## 访问地址

启动后访问：http://localhost:8188

## 参考

- [ComfyUI 官方仓库](https://github.com/comfyanonymous/ComfyUI)
- [AMD ROCm PyTorch 安装指南](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html)
- [ComfyUI AMD ROCm 支持公告](https://blog.comfy.org/p/official-amd-rocm-support-arrives)
- [ComfyUI 文档](https://docs.comfy.org/)
