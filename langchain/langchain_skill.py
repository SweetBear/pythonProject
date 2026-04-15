#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：langchain_skill.py
@Author  ：BillFang
@Date    ：2026/4/15 09:37
@Description :
"""
import json
from langchain_core.output_parsers import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate

from config_loader import ConfigLoader
import openai
from langchain_openai import ChatOpenAI
from utils.weather_util import get_city_weather_data

def direct_question(client):
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个全能的智能助手。"),
        ("system", "请你查一下{city}的天气。")
    ])

    message = chat_template.format_messages(city="扬州")

    response = client.invoke(message)

    return response.content

def final_resonse(client, ai_msg):
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "这是实时的{city}的天气数据，信息来源于Openweather API：https://api.openweathermap.org/data/2.5/weather，详细数据为：{detail}。"),
        ("system", "请你解析一下该数据，以自然语言的形式输出。")
    ])

    message = chat_template.format_messages(city=ai_msg["name"], detail=ai_msg)

    response = client.invoke(message)

    return response.content


if __name__ == '__main__':
    # 1. 加载配置（第一次会读文件，之后直接用缓存）
    config = ConfigLoader()
    xiaomi_cfg = config.get_xiaomi_config()

    openai.api_key = xiaomi_cfg["api_key"]
    openai.api_base_url = xiaomi_cfg["api_base_url"]
    client = ChatOpenAI(api_key=openai.api_key, base_url=openai.api_base_url, model=xiaomi_cfg["model"])

    tools = [get_city_weather_data]

    #绑定tools
    client_with_tool = client.bind_tools(tools)

    chain = client_with_tool | JsonOutputKeyToolsParser(key_name="get_city_weather_data", first_tool_only=True) | get_city_weather_data

    weather_str = chain.invoke("今天扬州天气怎么样？")
    print(weather_str)
    # 数据增强
    reponse = final_resonse(client, weather_str)

    print("使用天气查询skill返回的结果：")
    print(reponse)
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++")
    reponse = direct_question(client)
    print("直接询问大模型天气得到的结果：")
    print(reponse)

