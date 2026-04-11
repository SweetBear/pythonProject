#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/8 下午3:24
@Author  : Bill Fang
@File    : CancerDeal.py
@Desc    :
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    column_names = ['Block thickness（肿块厚度）', 'Cell size uniformity（细胞大小均匀性）',
       'Uniformity of cell morphology（细胞形态的均匀性）', 'Edge adhesion（边缘粘连）',
       'Single epithelial cell size（单一上皮细胞大小）', 'Naked nucleus（裸核）',
       'Bland Chromatin（平淡的染色质）', 'Normal nucleoli（正常核仁）',
       'Nuclear fission（核裂变）', 'class（良性2 恶性 4）']
    data = pd.read_excel('E:\\face_test\\breast_cancer_wisconsin.xlsx', sheet_name='she', header=0)

    X_train,X_test, y_train, y_test = train_test_split(data[column_names[1:9]], data[column_names[9]], test_size=0.25, random_state=33)


    ss = StandardScaler()

    print(X_train)
    X_train = ss.fit_transform(X_train)
    print(X_train)
    X_test = ss.transform(X_test)

    print("----->")
    print(X_test)