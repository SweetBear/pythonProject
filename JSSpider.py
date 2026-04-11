#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/20 下午3:30
@Author  : Bill Fang
@File    : JSSpider.py
@Desc    : 
"""

import requests
from urllib import request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

url = 'https://syly.lianchuanghj.com/syjs-client-newh5/#/bookingIndex?resId=1506&resName=%E5%BE%B7%E5%9F%BA%E8%89%BA%E6%9C%AF%E5%8D%9A%E7%89%A9%E9%A6%86'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Syly-Client':'newh5',
        'X-Syly-Version':'100',
        'Sec-Ch-Ua-Platform':'Android',
        'X-Requested-With':'XMLHttpRequest',
        'Origin':'https://syly.lianchuanghj.com',
        'Accept':'application/json',
        'Content-Type':'application/json',
        'Referer':'https://syly.lianchuanghj.com/syjs-client-newh5/'
           }

cookie = 'qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_c4d58350-34dc-11ed-b739-e55eae900f49=b4581c12-04f9-425b-b598-00d8447c0dea; qimo_seosource_c4d58350-34dc-11ed-b739-e55eae900f49=%E7%AB%99%E5%86%85; qimo_seokeywords_c4d58350-34dc-11ed-b739-e55eae900f49=; qimo_xstKeywords_c4d58350-34dc-11ed-b739-e55eae900f49=; href=https%3A%2F%2Fsyly.lianchuanghj.com%2Fsyjs-client-newh5%2F%23%2F; accessId=c4d58350-34dc-11ed-b739-e55eae900f49; pageViewNum=1'


def dealCokie(cookie):
    cookies = {}
    for line in cookie.split(';'):
        if line.strip():
            key, value = line.strip().split('=', 1)
            cookies[key] = value
    return cookies

if __name__ == '__main__':
    cookies = dealCokie(cookie)
    print(cookies)
    #获取总页数
    req = requests.get(url, headers=headers, cookies=cookies)
    #source_code = request.urlopen(req).read().decode('utf-8')
    #plain_text = str(source_code)
    print(req.text.encode('utf-8'))