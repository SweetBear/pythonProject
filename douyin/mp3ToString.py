#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：mp3ToString.py
@Author  ：BillFang
@Date    ：2026/4/13 13:43
@Description :
"""

import whisper
from faster_whisper import WhisperModel
from tqdm import tqdm

audio_path = "D:\\pythonTool\\345.mp3"
'''# 2. 加载模型（base / small / medium / large 越大越准）
model = whisper.load_model("base")

# 3. 转文字
result = model.transcribe(audio_path)

# 4. 输出并保存
text = result["text"]
print("提取文字：")
print(text)

with open("D:\\pythonTool\\视频文字.txt", "w", encoding="utf-8") as f:
    f.write(text)'''

# ======================
# 超强配置：准、快、带标点
# ======================
model = WhisperModel(
    model_size_or_path="large-v3",
    device="cpu",
    compute_type="int8"  # 速度最快
)

# 开始识别
segments, info = model.transcribe(
    audio_path,
    language="zh",  # 强制中文
    beam_size=3,  # 更准
    vad_filter=False,  # 过滤静音
    temperature=0.0,  # 固定温度，避免重复推理，加速
    word_timestamps=False,
    initial_prompt="以下是普通话语音转写，请使用标准标点符号，断句自然。"  # 强制加标点
)

# 输出带标点、流畅的文本

result_text = ""
with tqdm(total=info.duration, desc="转写中") as pbar:
    for seg in segments:
        result_text += seg.text + " "
        pbar.update(seg.end - seg.start)
print("转写结果：")
print(result_text)
with open("D:\\pythonTool\\视频文字3.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
