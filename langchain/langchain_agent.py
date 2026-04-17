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
from typing import Annotated, Literal

# 第三方库导入
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

# 本地模块导入
from init_llm import init_llm_with_tools
from weather_util import get_city_weather_data

# 常量定义
SYSTEM_PROMPT = "你是一个非常厉害的AI助手，但不了解实时的一些知识"
ENTRY_POINT_NODE = "agent"
TOOL_NODE = "tools"
END_NODE = "end"

# 初始化LLM实例
llm_with_tools = init_llm_with_tools()


def agent_node(state: MessagesState) -> dict:
    """
    LangGraph Agent节点处理函数

    Args:
        state: 包含对话消息的状态对象

    Returns:
        dict: 包含LLM响应消息的状态更新字典
    """
    try:
        # 构建消息列表
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

        # 调用LLM获取响应
        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}
    except Exception as e:
        error_msg = f"Agent节点处理失败: {e}"
        print(error_msg)
        return {"messages": [HumanMessage(content=error_msg)]}


def should_continue(state: MessagesState) -> Annotated[str, Literal[TOOL_NODE, END_NODE]]:
    """
    决策函数：判断是否需要调用工具

    Args:
        state: 包含对话消息的状态对象

    Returns:
        str: 下一个节点名称（"tools" 或 "end"）
    """
    try:
        last_message = state["messages"][-1]
        # 如果有工具调用请求，返回工具节点，否则结束流程
        return TOOL_NODE if last_message.tool_calls else END_NODE
    except IndexError:
        print("状态中没有消息，结束流程")
        return END_NODE
    except Exception as e:
        print(f"决策函数执行失败: {e}")
        return END_NODE


def build_workflow() -> StateGraph:
    """
    构建LangGraph工作流

    Returns:
        StateGraph: 编译后的工作流应用
    """
    # 创建状态图
    workflow = StateGraph(MessagesState)

    # 添加节点
    workflow.add_node(ENTRY_POINT_NODE, agent_node)
    workflow.add_node(TOOL_NODE, ToolNode([get_city_weather_data]))

    # 设置入口点
    workflow.set_entry_point(ENTRY_POINT_NODE)

    # 添加条件边
    workflow.add_conditional_edges(
        source=ENTRY_POINT_NODE,
        path=should_continue,
    )

    # 添加工具节点到agent节点的边
    workflow.add_edge(TOOL_NODE, ENTRY_POINT_NODE)

    return workflow.compile()


def main():
    """主函数：执行天气查询示例"""
    try:
        # 构建工作流
        app = build_workflow()

        # 执行查询
        query = "今天北京和扬州的天气比较，哪个城市的天气更适合出去踏青？"
        result = app.invoke({
            "messages": [HumanMessage(content=query)]
        }, debug=True)

        # 输出结果
        print("查询结果：")
        print(result["messages"][-1].content)

    except Exception as e:
        print(f"程序执行失败: {e}")


if __name__ == '__main__':
    main()
