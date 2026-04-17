#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：baidupanutil.py
@Author  ：BillFang
@Date    ：2026/4/14 13:32
@Description :
"""
from dupan import DuPanFileSystem
import os
import requests


def get_baidu_file_list(access_token, bduss, file_path):
    # 1. 登录（用BDUSS）
    cookie = "BDUSS=" + bduss + "; STOKEN=" + access_token
    fs = DuPanFileSystem.login(cookie)

    # 2. 获取文件直链 dlink
    dlink = fs.get_url(file_path)
    print(dlink)
    return dlink
    # 3. Aria2 RPC 下载（不限速）
    ##aria2.add_uri(dlink, save_dir="./downloads", options={"max-connection-per-server": "16"})


def python_download(file_url, save_path, access_token):
    save_dir = os.path.dirname(save_path)
    os.makedirs(save_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://pan.baidu.com/",
        "Host": "d.pcs.baidu.com",
        "Cookie": ""  # 带上token
    }

    # 流式下载，支持断点续传
    with requests.get(file_url, headers=headers, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB分块
                if chunk:
                    f.write(chunk)
    print(f"✅ 下载完成：{save_path}")


if __name__ == '__main__':
    aubss = ""
    access_token = ""
    file_path = "/照片/1476282810035.jpeg"
    file_url = get_baidu_file_list(access_token, aubss, file_path)
    python_download(file_url, "D:/123/tmp.jpg", access_token)
    print(file_url)
