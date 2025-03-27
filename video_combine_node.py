import os
import sys
import json
import numpy as np
import datetime
import torch
from PIL import Image
import itertools
import folder_paths
from typing import List
import cv2

class VideoCombineNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "frame_rate": ("FLOAT", {"default": 8, "min": 1, "step": 1}),
                "filename_prefix": ("STRING", {"default": "AnimateDiff"}),
                "format": (["video/mp4", "video/avi", "video/mkv", "video/mov", "video/wmv"], {}),
                "pingpong": ("BOOLEAN", {"default": False}),
                "save_output": ("BOOLEAN", {"default": True}),
                "custom_output_path": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filename",)
    OUTPUT_NODE = True
    CATEGORY = "Video"
    FUNCTION = "combine_video"

    def combine_video(self, images, frame_rate, filename_prefix="AnimateDiff", 
                     format="video/mp4", pingpong=False, save_output=True, custom_output_path=""):
        # 设置输出目录
        if custom_output_path and os.path.isdir(custom_output_path):
            output_dir = custom_output_path
        else:
            output_dir = folder_paths.get_output_directory() if save_output else folder_paths.get_temp_directory()

        os.makedirs(output_dir, exist_ok=True)

        # 直接使用文件名，不添加计数器
        file = f"{filename_prefix}.mp4"
        file_path = os.path.join(output_dir, file)

        # 处理图像数据
        if isinstance(images, torch.Tensor):
            images = images.cpu().numpy()
        images = (images * 255).astype(np.uint8)
        
        # 处理 pingpong 效果
        if pingpong:
            images = np.concatenate([images, images[-2:0:-1]])

        # 获取视频尺寸
        height, width = images[0].shape[:2]
        
        # 根据格式选择对应的编码器和文件扩展名
        format_configs = {
            "video/mp4": ("mp4v", "mp4"),
            "video/avi": ("XVID", "avi"),
            "video/mkv": ("X264", "mkv"),
            "video/mov": ("mp4v", "mov"),
            "video/wmv": ("WMV2", "wmv")
        }
        
        codec, ext = format_configs[format]
        file = f"{filename_prefix}.{ext}"
        file_path = os.path.join(output_dir, file)

        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(file_path, fourcc, frame_rate, (width, height))

        # 写入帧
        for img in images:
            # OpenCV 使用 BGR 格式，需要转换
            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            out.write(frame)

        # 释放资源
        out.release()

        return (file_path,)

    def _get_next_counter(self, output_dir, filename_prefix):
        max_counter = 0
        for f in os.listdir(output_dir):
            if f.startswith(filename_prefix):
                try:
                    counter = int(f.split("_")[-1].split(".")[0])
                    max_counter = max(max_counter, counter)
                except:
                    pass
        return max_counter + 1

NODE_CLASS_MAPPINGS = {
    "VideoCombine": VideoCombineNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoCombine": "Video Combine"
}