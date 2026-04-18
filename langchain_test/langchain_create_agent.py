#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：langchain_agent.py
@Author  ：BillFang
@Date    ：2026/4/17 13:58
@Description : LangGraph Agent 实现天气查询功能
"""

# 标准库导入

from langchain.agents import create_agent
# 第三方库导入
from langchain_core.messages import SystemMessage, HumanMessage

# 本地模块导入
from init_llm import init_llm
from weather_util import get_city_weather_data

# 常量定义
SYSTEM_PROMPT = "你是一个非常厉害的AI助手，但不了解实时的一些知识"
ENTRY_POINT_NODE = "agent"
TOOL_NODE = "tools"
END_NODE = "end"

# 初始化LLM实例
llm = init_llm()

def main():
    """主函数：执行天气查询示例"""
    try:
        # 构建工作流
        agent = create_agent(
            llm,
            tools=[get_city_weather_data],
            system_prompt="你是一个非常厉害的AI助手，但不了解实时的一些知识"
        )

        # 执行查询
        query = "今天北京和扬州的天气比较，哪个城市的天气更适合出去踏青？"
        result = agent.invoke(
            {"messages": [HumanMessage("今天北京和扬州的天气比较，哪个城市的天气更适合出去踏青？")]}
        , debug=True)
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"程序执行失败: {e}")


if __name__ == '__main__':
    main()
