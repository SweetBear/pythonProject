#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/19 下午3:55
@Author  : Bill Fang
@File    : ExcelDeal.py
@Desc    : 
"""
from openpyxl import Workbook,load_workbook
import mysql.connector
import requests
import os


def get_url_img(url, out_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(out_path, 'wb') as f:
            f.write(response.content)  # 将获取到的图片内容写入文件


if __name__ == '__main__':

    # 创建数据库连接
    db = mysql.connector.connect(
        host="",  # MySQL服务器地址
        port="",  # MySQL服务器端口
        user="",  # 用户名
        password="",  # 密码
        database=""  # 数据库名称
    )

    # 创建游标对象，用于执行SQL查询
    cursor = db.cursor()

    # 查询所有记录
    cursor.execute("SELECT t.stu_code,t.cover,t.stu_name,r.name as class_name,e.grade_name FROM org_student t left join org_class_info r on r.`code`=t.class_code left join org_grade e on e.grade_code=t.grade_code where t.isdel=0 and t.org_code='8ce5652a58e8414bb54f21c17d44ab13' and t.cover is not null and t.cover !='' order by e.grade_name,r.name")

    # 获取查询结果
    results = cursor.fetchall()

    i = 0
    for row in results:
        i = i + 1
        #print(str(i) + "-->" + key + "-->" + stu_dict[key])
        student_name = row[2]
        cover_url = row[1]
        class_name = row[4] + row[3]
        img_type = cover_url.split('.')[len(cover_url.split('.')) - 1]

        output_path = 'E:\\face_test\\淮安市新淮高级中学\\' + class_name + "\\"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_name = output_path + student_name + '.' + img_type
        #print(output_name)
        get_url_img(cover_url, output_path + student_name + '.' + img_type)

        print(student_name + "--->" + class_name + "--->" + cover_url)



