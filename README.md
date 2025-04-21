# comfyui_video_BC

这是一个针对[ComfyUI](https://github.com/comfyanonymous/ComfyUI)的视频工作流程的自定义节点包，包含两个节点：一个用于批量加载视频帧，另一个用于将图像序列保存为视频，具有自定义设置。

## 🧩 包含的节点

### 1. VideoSequenceProcessor
- 新增设置导入视频强制帧率选项
- 从目录中的多个视频加载帧。
- 模式：按索引加载、自动下一个或随机选择。
- 可选的尺寸调整、帧限制和帧率覆盖。
- 适用于数据集准备和动画工作流程。

### 2. VideoCombine
- 将图像序列（例如来自AnimateDiff的图像）转换为视频。
- 支持多种格式：MP4、AVI、MKV、MOV、WMV。
- 可选的“乒乓”循环。
- 可自定义文件名和输出路径。

## 📦 安装
将这些Python文件放入`ComfyUI/custom_nodes`目录中。

## 🔧 依赖
确保已安装OpenCV和其他依赖项：
```bash
git clone https://github.com/JioJe/comfyui_video_BC
```
B站节点讲解链接：https://www.bilibili.com/video/BV1heZVY3E8o/?spm_id_from=333.1387.homepage.video_card.click&vd_source=cfcf2acc406e911d0270e4c5832b80a8

These are two custom nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) designed to streamline video workflows: one for batch loading video frames and one for saving image sequences as videos with custom settings.

## 🧩 Nodes Included

### 1. VideoSequenceProcessor
- Load frames from multiple videos in a directory.
- Modes: load by index, auto-next, or random selection.
- Optional resize, frame limit, and frame rate override.
- Ideal for dataset preparation and animation workflows.

### 2. VideoCombine
- Convert image sequences (e.g., from AnimateDiff) into a video.
- Supports multiple formats: MP4, AVI, MKV, MOV, WMV.
- Optional "ping-pong" looping.
- Customizable filename and output path.

## 📦 Installation
Place these Python files into your `ComfyUI/custom_nodes` directory.

## 🔧 Requirements
Ensure you have OpenCV and other dependencies installed:
```bash
git clone https://github.com/JioJe/comfyui_video_BC

