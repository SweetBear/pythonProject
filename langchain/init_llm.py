# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：init_llm.py
@Author  ：BillFang
@Date    ：2026/4/17 15:38
@Description :
"""
from typing import Any, Sequence

from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from config_loader import ConfigLoader
from weather_util import get_city_weather_data


def load_llm_config() -> dict:
    """
    加载LLM配置信息

    Returns:
        dict: 包含api_key、base_url、model的配置字典
    """
    try:
        config_loader = ConfigLoader()
        xiaomi_config = config_loader.get_xiaomi_config()
        return {
            "api_key": xiaomi_config["api_key"],
            "base_url": xiaomi_config["api_base_url"],
            "model": xiaomi_config["model"]
        }
    except KeyError as e:
        raise ValueError(f"配置文件缺少必要的键: {e}")
    except Exception as e:
        raise RuntimeError(f"加载配置失败: {e}")


def init_llm() -> ChatOpenAI:
    """
    初始化LLM实例并绑定工具

    Returns:
        ChatOpenAI: 绑定了天气查询工具的LLM实例
    """
    llm_config = load_llm_config()
    llm = ChatOpenAI(
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"],
        model=llm_config["model"]
    )
    return llm


def init_llm_with_tools() -> Runnable[PromptValue | str | Sequence[Any], AIMessage]:
    # 绑定工具
    llm = init_llm()
    tools = [get_city_weather_data]
    return llm.bind_tools(tools)
