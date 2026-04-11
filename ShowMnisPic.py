#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/3/12 下午4:06
@Author  : Bill Fang
@File    : TorchTensorTest.py
@Desc    : 
"""
import gzip
import numpy as np
import matplotlib.pyplot as plt

# 读取图片文件
def read_mnist_images(filename):
    with gzip.open(filename, 'rb') as f:
        f.read(16)  # 跳过前16字节头部
        buf = f.read()
    data = np.frombuffer(buf, dtype=np.uint8)
    data = data.reshape(-1, 28, 28)  # (N, 28, 28)
    return data

# 读取标签文件
def read_mnist_labels(filename):
    with gzip.open(filename, 'rb') as f:
        f.read(8)   # 跳过前8字节头部
        buf = f.read()
    labels = np.frombuffer(buf, dtype=np.uint8)
    return labels

# 你的路径（和你下载的4个gz文件一致）
train_images = read_mnist_images('D:/dataSet/MNIST/raw/train-images-idx3-ubyte.gz')
train_labels = read_mnist_labels('D:/dataSet/MNIST/raw/train-labels-idx1-ubyte.gz')

# 看第 0 张图片（可以改成 1,2,3,... 看不同数字）
print(train_images[0].shape)

'''plt.figure(figsize=(10, 10))
for i in range(100):
    plt.subplot(10, 10, i+1)
    plt.imshow(train_images[i], cmap='gray')
    plt.title(train_labels[i])
    plt.axis('off')
plt.tight_layout()
plt.show()'''