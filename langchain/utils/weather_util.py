#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：weather_util.py
@Author  ：BillFang
@Date    ：2026/4/15 09:19
@Description :
"""

import requests
from langchain_core.tools import tool

class OpenWeather():
    def __init__(self, APPID):
        self.app_id = APPID


    def get_lat_lon(self, city_name):
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": city_name,
            "limit": 1,
            "appid": self.app_id,
        }
        try:
            res = requests.get(geo_url, params=params)
            res.raise_for_status()
            data = res.json()
            if not data:
                print("未找到该城市")
                return None, None
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            name = data[0]["name"]
            country = data[0]["country"]
            print(f"定位成功：{name}, {country}")
            return lat, lon
        except Exception as e:
            print("获取经纬度失败:", e)
            return None, None
@tool
def get_city_weather_data(city_name) -> dict:
    """
        调用 OpenWeatherMap API 获取指定经纬度的天气信息
        :param lat: 纬度
        :param lon: 经度
        :param appid: OpenWeatherMap 申请的 API Key
        :return: 天气数据字典 / None
        """
    weather_client = OpenWeather(APPID='ab203b794f7b27b777bb48f4eb30838c')
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    lat, lon = weather_client.get_lat_lon(city_name)
    # 请求参数
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weather_client.app_id,
        "units": "metric",  # 单位：metric=摄氏度，imperial=华氏度，默认开尔文
        "lang": "zh_cn"  # 返回中文描述
    }

    try:
        # 发送 GET 请求
        response = requests.get(base_url, params=params)
        # 检查请求是否成功
        response.raise_for_status()
        # 解析 JSON 数据
        weather_data = response.json()
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")
        return None

if __name__ == '__main__':
    #方法加上@tool时必须使用.invlke方法调用
    print(get_city_weather_data.invoke('扬州'))

