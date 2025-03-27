# comfyui_video_BC

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
