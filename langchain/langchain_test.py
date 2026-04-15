#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：langchain_test.py
@Author  ：Administrator
@Date    ：2026/4/11 14:11
@Description :
"""
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
import openai
from config_loader import ConfigLoader
from langchain_core.prompts import ChatPromptTemplate

# 1. 加载配置（第一次会读文件，之后直接用缓存）
config = ConfigLoader()
xiaomi_cfg = config.get_xiaomi_config()

openai.api_key = xiaomi_cfg["api_key"]
openai.api_base_url = xiaomi_cfg["api_base_url"]
client = ChatOpenAI(api_key=openai.api_key, base_url=openai.api_base_url, model=xiaomi_cfg["model"])

message = [HumanMessage(content="查一下北京今天的天气")]

#等执行结束打印
aiResponse = client.invoke(message)
print(aiResponse)
print(aiResponse.content)

#stram打印
#for chunk in client.stream(message):
    #print(chunk.content, end="", flush=True)

#使用prompt_template
#message = [
    #{"role":"system","content":"你是一个AI智能助手，你的名字叫{name}"},
    #{"role":"human","content":"请给我讲解一下{user_name}"}
#]
#prompt_template = ChatPromptTemplate.from_messages(message)

#prompt = prompt_template.format_messages(name="小M", user_name="LangChain")

#print(prompt_template)
#print(prompt)

#for chunk in client.stream(prompt):
    #print(chunk.content, end="", flush=True)