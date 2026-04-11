#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：FewShot.py
@Author  ：Administrator
@Date    ：2026/4/11 16:15
@Description :
"""
import openai
from config_loader import ConfigLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

def few_shot_input(input):

    # 1. 定义【小样本例子】——核心！给AI看的案例
    examples = [
        {
            "text": "今天心情特别好",
            "label": "积极"
        },
        {
            "text": "上班迟到还下雨，好烦",
            "label": "消极"
        },
        {
            "text": "天气一般，没什么感觉",
            "label": "中性"
        }
    ]

    # 2. 定义例子的格式模板
    example_prompt = PromptTemplate(
        input_variables=["text", "label"],
        template="文本：{text}\n情感：{label}\n"
    )

    # 3. 组装 FewShot 模板（例子 + 提示 + 待预测内容）
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,               # 小样本
        example_prompt=example_prompt,   # 例子格式
        prefix="请判断以下文本的情感，只能输出：积极/消极/中性",  # 开头指令
        suffix="文本：{input}\n情感：",    # 待预测内容
        input_variables=["input"],       # 输入变量
        example_separator="\n"           # 例子之间分隔符
    )

    # 4. 生成最终提示词
    prompt = few_shot_prompt.format(input=input)
    return prompt

#对比没有few-shot功能



if __name__ == '__main__':
    # 1. 加载配置（第一次会读文件，之后直接用缓存）
    config = ConfigLoader()
    xiaomi_cfg = config.get_xiaomi_config()

    openai.api_key = xiaomi_cfg["api_key"]
    openai.api_base_url = xiaomi_cfg["api_base_url"]
    client = ChatOpenAI(api_key=openai.api_key, base_url=openai.api_base_url, model=xiaomi_cfg["model"])
    input = "这个电影太好看了！"
    # 不用few-shot
    print("不用few-shot输出：" + client.invoke(input).content)
    #使用few-shot
    prompt = few_shot_input(input)
    print("-------------------------------")
    print("使用few-shot的输出：" + client.invoke(prompt).content)

