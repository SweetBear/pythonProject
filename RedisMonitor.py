#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/1 下午4:51
@Author  : Bill Fang
@File    : RedisMonitor.py
@Desc    : 
"""

import os

if __name__ == '__main__':
    os.chdir('D:/learnTool/redis')
    cmd = 'start cmd.exe /K redis-server redis.windows.conf'
    result = os.system(cmd)

    print(result)
