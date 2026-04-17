#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/19 下午3:55
@Author  : Bill Fang
@File    : ExcelDeal.py
@Desc    : 
"""
from faker import Faker
from faker.providers import BaseProvider


class CustomProvider(BaseProvider):
    def pystr(self):
        return "这是一个自定义字符串"


if __name__ == '__main__':
    faker = Faker(locale="zh_CN")
    print(
        faker.name() + "==>" + faker.address() + "==>" + faker.city_name() + "==>" + faker.company() + "==>" + faker.job() + "==>" + faker.phone_number() + "==>" + faker.ssn(
            min_age=18, max_age=70))

    # 使用Faker时注册自定义提供程序
    fake = Faker()
    fake.add_provider(CustomProvider)

    print(fake.pystr())  # 输出: 这是一个自定义字符串
