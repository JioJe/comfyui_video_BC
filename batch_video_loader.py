import os
import torch
import numpy as np
import cv2
from PIL import Image
import folder_paths

BIGMAX = 9999999
DIMMAX = 8192

class BatchVideoLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {
                    "placeholder": "视频文件夹路径",
                    "default": folder_paths.get_input_directory(),
                }),
                "video_index": ("INT", {"default": 0, "min": 0, "max": BIGMAX, "step": 1}),  # 添加视频索引参数
                "frames_per_batch": ("INT", {"default": 8, "min": 1, "max": 32, "step": 1}),
                "frame_load_cap": ("INT", {"default": 0, "min": 0, "max": BIGMAX, "step": 1}),
                "custom_width": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
                "custom_height": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
                "frame_rate": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("frames",)
    FUNCTION = "load_video_batch"
    CATEGORY = "加载器/视频"

    @classmethod
    def load_video_batch(cls, directory, video_index=0, frames_per_batch=8, frame_load_cap=0, custom_width=0, custom_height=0, frame_rate=0.0):
        if not directory or not isinstance(directory, str):
            directory = folder_paths.get_input_directory()
        
        if not os.path.isdir(directory):
            raise ValueError(f"目录不存在: {directory}")

        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        video_files = []
        for file in os.listdir(directory):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(os.path.join(directory, file))

        if not video_files:
            raise ValueError(f"在目录 {directory} 中未找到视频文件")

        if video_index >= len(video_files):
            raise ValueError(f"视频索引 {video_index} 超出范围，共找到 {len(video_files)} 个视频")

        cap = cv2.VideoCapture(video_files[video_index])
        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {video_files[video_index]}")

        frames_batch = []
        while len(frames_batch) < frames_per_batch:
            ret, frame = cap.read()
            if not ret:
                break

            if custom_width > 0 and custom_height > 0:
                frame = cv2.resize(frame, (custom_width, custom_height))
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames_batch.append(frame)

            if frame_load_cap > 0 and len(frames_batch) >= frame_load_cap:
                break

        cap.release()

        if not frames_batch:
            raise ValueError("无法读取视频帧")

        frames_tensor = torch.from_numpy(np.stack(frames_batch))
        return (frames_tensor,)

    @classmethod
    def IS_CHANGED(cls, directory, **kwargs):
        if not directory or not isinstance(directory, str):
            directory = folder_paths.get_input_directory()
        if not os.path.isdir(directory):
            return ""
        return os.path.getmtime(directory)

    @classmethod
    def VALIDATE_INPUTS(cls, directory, **kwargs):
        if not directory or not isinstance(directory, str):
            directory = folder_paths.get_input_directory()
        if not os.path.isdir(directory):
            return "无效的目录路径: {}".format(directory)
        return True

class VideoSequenceProcessor:
    # 添加持久化的类变量
    _current_index = 0
    _last_directory = None
    _video_files = []

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {
                    "placeholder": "视频文件夹路径",
                    "default": folder_paths.get_input_directory(),
                }),
                "mode": (["单个视频", "下一个视频", "随机视频"], {"default": "单个视频"}),
                "video_index": ("INT", {"default": 0, "min": 0, "max": BIGMAX, "step": 1}),
                "frames_per_video": ("INT", {"default": 8, "min": 1, "max": BIGMAX, "step": 1}),  # 修改为无上限
                "custom_width": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
                "custom_height": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "STRING")
    RETURN_NAMES = ("frames", "current_index", "total_videos", "filename_text")
    FUNCTION = "process_sequence"
    CATEGORY = "加载器/视频"

    @classmethod
    def process_sequence(cls, directory, mode="单个视频", video_index=0, frames_per_video=8, custom_width=0, custom_height=0):
        if not os.path.isdir(directory):
            raise ValueError(f"目录不存在: {directory}")

        # 检查目录是否改变
        if cls._last_directory != directory:
            cls._current_index = 0
            cls._last_directory = directory
            # 重新扫描视频文件
            cls._video_files = []
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
            for file in os.listdir(directory):
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    cls._video_files.append(os.path.join(directory, file))

        if not cls._video_files:
            raise ValueError(f"在目录 {directory} 中未找到视频文件")

        # 根据模式选择视频
        if mode == "单个视频":
            selected_index = min(video_index, len(cls._video_files) - 1)
        elif mode == "下一个视频":
            selected_index = cls._current_index
            cls._current_index = (cls._current_index + 1) % len(cls._video_files)
        else:  # 随机视频
            selected_index = np.random.randint(0, len(cls._video_files))

        video_path = cls._video_files[selected_index]
        filename = os.path.basename(video_path)  # 获取文件名
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {video_path}")

        frames = []
        frame_count = 0
        while frame_count < frames_per_video:
            ret, frame = cap.read()
            if not ret:
                break

            if custom_width > 0 and custom_height > 0:
                frame = cv2.resize(frame, (custom_width, custom_height))
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
            frame_count += 1

        cap.release()

        if not frames:
            raise ValueError("无法读取视频帧")

        frames_tensor = torch.from_numpy(np.stack(frames))
        return (frames_tensor, selected_index, len(cls._video_files), filename)

    @classmethod
    def IS_CHANGED(cls, directory, mode, **kwargs):
        if mode == "下一个视频":
            # 对于"下一个视频"模式，每次都返回不同的值以触发更新
            return float("nan")
        return super().IS_CHANGED(directory, **kwargs)
# 更新节点映射
NODE_CLASS_MAPPINGS = {
    "BatchVideoLoader": BatchVideoLoader,
    "VideoSequenceProcessor": VideoSequenceProcessor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchVideoLoader": "批量视频加载器 🎥",
    "VideoSequenceProcessor": "视频序列处理器 🎬"
}