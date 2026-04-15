#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：baidupanutil.py
@Author  ：BillFang
@Date    ：2026/4/14 13:32
@Description :
"""
import json
import requests
import os


def get_baidi_dlink(file_path:str, access_token:str) -> str:
    """
        stoken:
        通过百度开放 API 获取文件直链 dlink
        """
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "filemetas",
        "access_token": access_token,
        "path": file_path,
        "need_dlink": 1
    }
    headers = {
        "Accept-Encoding": "identity",
        "User-Agent": "pan.baidu.com",
        "Referer": "https://pan.baidu.com/"
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except json.JSONDecodeError:
        print(f"响应非JSON，内容: {resp.text[:200]}")  # 只打印前200字符
        return None


def get_baidu_file_list(access_token, target_path):
    """
    获取指定路径下的文件列表，找到目标文件的fsid
    :param access_token: 你的token
    :param target_path: 目标文件路径（如 /照片/1476283115067.jpeg）
    """
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    # 先提取文件所在目录（比如文件在/照片下，目录就是/照片）
    import os
    dir_path = os.path.dirname(target_path)

    params = {
        "method": "list",
        "access_token": access_token,
        "dir": dir_path,
        "web": 1
    }
    headers = {
        "User-Agent": "pan.baidu.com",
        "Referer": "https://pan.baidu.com/"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        file_list = resp.json().get("list", [])

        # 遍历找到目标文件
        for file in file_list:
            if file.get("path") == target_path:
                return file.get("fs_id")  # 返回正确的fsid
        print(f"未找到目标文件：{target_path}")
        return None
    except Exception as e:
        print(f"获取文件列表失败：{e}")
        return None



def get_baidu_dlink(access_token, target_file_path):
    # 1. 先获取正确的fsid
    fs_id = get_baidu_file_list(access_token, target_file_path)
    if not fs_id:
        return None

    # 2. 正确的下载接口配置
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "filemetas",
        "access_token": access_token,
        "fsids": f"[{fs_id}]",  # 关键：数组格式
        "dlink": 1
    }
    headers = {
        "Accept-Encoding": "identity",
        "User-Agent": "pan.baidu.com",
        "Referer": "https://pan.baidu.com/"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        # 检查是否有错误码
        if result.get("errno") != 0:
            print(f"API返回错误：{result}")
            return None

        # 返回下载链接信息
        return result
    except Exception as e:
        print(f"请求失败：{e}")
        return None


def get_baidu_file_list(access_token, dir_path="/"):
    """
    获取指定目录下的所有文件/文件夹，打印列表方便核对
    """
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "list",
        "access_token": access_token,
        "dir": dir_path,
        "web": 1
    }
    headers = {
        "User-Agent": "pan.baidu.com",
        "Referer": "https://pan.baidu.com/"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if result.get("errno") != 0:
            print(f"获取目录 {dir_path} 失败：{result}")
            return []

        file_list = result.get("list", [])
        print(f"\n=== 目录 {dir_path} 下的文件列表 ===")
        for f in file_list:
            print(f"路径: {f.get('path')}, fsid: {f.get('fs_id')}, 文件名: {f.get('filename')}")

        return file_list
    except Exception as e:
        print(f"请求异常：{e}")
        return []


def find_file_by_path(access_token, target_full_path):
    """
    递归查找目标文件，返回fsid
    """
    # 拆分路径：目录 + 文件名
    dir_path = os.path.dirname(target_full_path)
    filename = os.path.basename(target_full_path)

    # 处理根目录
    if dir_path == "":
        dir_path = "/"

    # 获取当前目录文件列表
    file_list = get_baidu_file_list(access_token, dir_path)

    # 查找匹配的文件
    for f in file_list:
        if f.get("filename") == filename and f.get("path") == target_full_path:
            print(f"\n✅ 找到目标文件！fsid: {f.get('fs_id')}")
            return f.get("fs_id")

    print(f"\n❌ 未找到目标文件：{target_full_path}")
    return None


def get_baidu_dlink(access_token, target_file_path):
    # 1. 查找文件fsid
    fs_id = find_file_by_path(access_token, target_file_path)
    if not fs_id:
        return None

    # 2. 调用filemetas获取下载链接
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "filemetas",
        "access_token": access_token,
        "fsids": f"[{fs_id}]",
        "dlink": 1
    }
    headers = {
        "Accept-Encoding": "identity",
        "User-Agent": "pan.baidu.com",
        "Referer": "https://pan.baidu.com/"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if result.get("errno") != 0:
            print(f"API返回错误：{result}")
            return None

        return result
    except Exception as e:
        print(f"请求失败：{e}")
        return None

if __name__ == '__main__':
    access_token = ""
    file_path = "/照片/1476282810035.jpeg"
    file_url = get_baidu_file_list(access_token)

    print(file_url)