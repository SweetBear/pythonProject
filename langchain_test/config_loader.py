#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Project ：pythonProject
@File    ：config_loader.py
@Author  ：Administrator
@Date    ：2026/4/11 14:39
@Description :
"""
import configparser
import os
from typing import Dict, Any


class ConfigLoader:
    # 单例模式：整个程序只加载一次配置，避免重复读文件
    _instance = None
    _config = None

    def __new__(cls, config_path: str = r"E:\pycharm_code\resources\config.properties"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path: str):
        """内部方法：加载配置文件，做基础校验"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"配置文件不存在: {os.path.abspath(config_path)}\n"
                "请在项目根目录创建 config.properties 文件，参考模板格式。"
            )

        # 用utf-8编码读取，避免中文乱码
        self._config = configparser.ConfigParser()
        self._config.read(config_path, encoding="utf-8")

    def get(self, section: str, key: str) -> str:
        """
        通用获取配置的方法
        :param section: 配置的分组（比如[xiaomi]就是"xiaomi"）
        :param key: 配置的键名（比如api_key）
        """
        try:
            return self._config[section][key].strip()
        except KeyError as e:
            raise ValueError(
                f"配置缺失: 找不到 [{section}] 下的 {key} 配置，请检查 config.ini"
            ) from e

    def get_xiaomi_config(self) -> Dict[str, Any]:
        """专门获取小米MiMo模型的完整配置，自动转换类型"""
        section = "xiaomi"
        # 必填配置
        config = {
            "api_key": self.get(section, "api_key"),
            "api_base_url": self.get(section, "api_base_url"),
            "model": self.get(section, "model"),
        }

        # 可选配置，带默认值，用户不写也不会报错
        try:
            config["temperature"] = float(self.get(section, "temperature"))
        except:
            config["temperature"] = 0.7

        try:
            config["max_tokens"] = int(self.get(section, "max_tokens"))
        except:
            config["max_tokens"] = 1024

        return config

    def get_openweather_config(self) -> Dict[str, Any]:
        section = "openweather"
        # 必填配置
        config = {
            "app_id": self.get(section, "app_id"),
        }

        return config
