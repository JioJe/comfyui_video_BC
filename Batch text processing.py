# Text Loader with Batch Output for ComfyUI
# 一次性读取文件夹内所有txt文件，批量输出文本内容和文件名

import os

class TextBatchLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
            },
            "hidden": {
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
    RETURN_TYPES = ("LIST", "LIST")
    RETURN_NAMES = ("texts", "filenames")
    FUNCTION = "load_texts"
    CATEGORY = "was-node-suite-comfyui"

    def load_texts(self, folder_path="", prompt=None, extra_pnginfo=None):
        if not folder_path:
            return ([], [])
        try:
            files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt') and os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            texts = []
            filenames = []
            for fname in files:
                fpath = os.path.join(folder_path, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        texts.append(f.read())
                    filenames.append(fname)
                except Exception as e:
                    texts.append(f"Error: {str(e)}")
                    filenames.append(fname)
            return (texts, filenames)
        except Exception as e:
            return ([f"Error: {str(e)}"], [])

class TextBatchIndexer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "batch_texts": ("LIST", {}),
                "batch_filenames": ("LIST", {}),
                "current_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
            },
        }
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "filename")
    FUNCTION = "get_by_index"
    CATEGORY = "was-node-suite-comfyui"

    def get_by_index(self, batch_texts, batch_filenames, current_index):
        n = len(batch_texts)
        if not batch_texts or not batch_filenames or n == 0 or current_index < 0 or current_index >= n:
            return ("", "")
        text = batch_texts[current_index]
        filename = batch_filenames[current_index]
        return (text, filename)

class TextBatchSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "batch_texts": ("LIST", {}),
                "save_dir": ("STRING", {"default": "./output", "multiline": False}),
                "filename_prefix": ("STRING", {"default": "file", "multiline": False}),
                "filename_sep": ("STRING", {"default": "_", "multiline": False}),
                "filename_pad": ("INT", {"default": 4, "min": 1, "max": 8}),
                "file_extension": ("STRING", {"default": ".txt", "multiline": False}),
                "encoding": ("STRING", {"default": "utf-8", "multiline": False}),
            },
            "optional": {
                "filename_suffix": ("STRING", {"default": "", "multiline": False}),
                "batch_filenames": ("LIST", {}),
            },
        }
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("saved_files",)
    FUNCTION = "save_batch"
    CATEGORY = "was-node-suite-comfyui"
    DESCRIPTION = "批量保存文本到文件，右端输出为可选，节点本身即可完成保存，无需下游节点消费。"

    def save_batch(self, batch_texts, save_dir, filename_prefix, filename_sep, filename_pad, file_extension, encoding, filename_suffix="", batch_filenames=None):
        import os
        import re
        from datetime import datetime
        now = datetime.now()
        save_dir = re.sub(r'\[time\((.*?)\)\]', lambda m: now.strftime(m.group(1)), save_dir)
        os.makedirs(save_dir, exist_ok=True)
        saved_files = []
        n = len(batch_texts)
        for i, text in enumerate(batch_texts):
            if batch_filenames and i < len(batch_filenames):
                base, _ = os.path.splitext(batch_filenames[i])
                fname = f"{filename_prefix}{filename_sep}{base}"
            else:
                idx_str = str(i+1).zfill(filename_pad)
                fname = f"{filename_prefix}{filename_sep}{idx_str}"
            if filename_suffix:
                fname += filename_suffix
            if not file_extension.startswith('.'):
                file_extension = '.' + file_extension
            fname += file_extension
            fpath = os.path.join(save_dir, fname)
            try:
                with open(fpath, "w", encoding=encoding) as f:
                    f.write(text)
                saved_files.append(fpath)
            except Exception as e:
                saved_files.append(f"Error: {str(e)}")
        return (saved_files,)

class TextBatchReplace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "batch_texts": ("LIST", {}),
                "搜索_1": ("STRING", {"default": ""}),
                "替换_1": ("STRING", {"default": ""}),
                "搜索_2": ("STRING", {"default": ""}),
                "替换_2": ("STRING", {"default": ""}),
                "搜索_3": ("STRING", {"default": ""}),
                "替换_3": ("STRING", {"default": ""}),
            },
        }
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("replaced_texts",)
    FUNCTION = "replace_batch"
    CATEGORY = "was-node-suite-comfyui"

    def replace_batch(self, batch_texts, 搜索_1, 替换_1, 搜索_2, 替换_2, 搜索_3, 替换_3):
        search_list = [搜索_1, 搜索_2, 搜索_3]
        replace_list = [替换_1, 替换_2, 替换_3]
        replaced = []
        for text in batch_texts:
            new_text = text
            for s, r in zip(search_list, replace_list):
                if s:
                    new_text = new_text.replace(s, r)
            replaced.append(new_text)
        return (replaced,)

NODE_CLASS_MAPPINGS = {
    "TextBatchLoader": TextBatchLoader,
    "TextBatchIndexer": TextBatchIndexer,
    "TextBatchSaver": TextBatchSaver,
    "TextBatchReplace": TextBatchReplace,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextBatchLoader": "批量文本读取",
    "TextBatchIndexer": "批量文本索引",
    "TextBatchSaver": "批量文本保存",
    "TextBatchReplace": "批量提示词替换",
}