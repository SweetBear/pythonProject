#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/3/12 下午4:06
@Author  : Bill Fang
@File    : TorchTensorTest.py
@Desc    : 
"""
import time

import torch
import numpy as np

import matplotlib.pyplot as plt

'''# 当前安装的 PyTorch 库的版本
print(torch.__version__)
# 检查 CUDA 是否可用，即你的系统有 NVIDIA 的 GPU
print(torch.cuda.is_available())
# 检查可用 GPU 数量
print(f"可用 GPU 数量: {torch.cuda.device_count()}")
# 获取第0个GPU的名称
gpu_name = torch.cuda.get_device_name(0)
print(f"GPU 0 Name: {gpu_name}")'''

# 张量
# 全是0张量
'''tmp = torch.zeros(2,3)
print(tmp)'''
# 全是1张量
'''tmp = torch.ones(2,3)
print(tmp)'''

# 使用numpy导入张量
'''num_arr = np.array([[1,2,3],[3,4,5]])
tmp = torch.from_numpy(num_arr)
print(tmp)'''

# 随机张量
'''time1 = time.time()
tmp = torch.randn(2,3)
time2 = time.time()
print(time2 - time1)
print(tmp)'''

# 在指定设备（CPU/GPU）上创建张量
'''time1 = time.time()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
d = torch.randn(2, 3, device=device)
torch.cuda.synchronize()
time2 = time.time()
print(time2 - time1)
print(d)'''

'''#张量操作
tmp1 = torch.rand(2,3)
tmp2 = torch.rand(2,3)
print(tmp1)
print(tmp2)
print(tmp1 + tmp2)

print(tmp1 * tmp2)
# 张量的转置
g = torch.randn(3, 2)
print(g)
print(g.t())
print(g.transpose(0, 1))

# 张量的形状
print(g.shape)'''

# 梯度和自动微分
'''# 创建一个需要梯度的张量
tensor_requires_grad = torch.tensor([1.0], requires_grad=True)
print(tensor_requires_grad)
# 进行一些操作
tensor_result = tensor_requires_grad * 2
# 计算梯度
tensor_result.backward()
print(tensor_requires_grad.grad)  # 输出梯度'''

'''# 创建一个需要计算梯度的张量
x = torch.tensor([2,2.],  requires_grad=True)
print(x)

# 执行某些操作
y = x + 2
z = y * y * 3
out = z.mean()

print(out)

# 反向传播，计算梯度
out.backward()

# 查看 x 的梯度
print(x.grad)'''

# 张量堆叠
'''tensor_2d = torch.tensor([
    [2,2,2,2,3],
    [4,5,6,7,8],
    [3,4,6,8,1]
])
tensor_3d = torch.stack([tensor_2d, tensor_2d +4, tensor_2d+1])
print(tensor_3d)
print(tensor_3d.shape)
print(tensor_3d.size())
print(tensor_3d.dtype)
print(tensor_3d.device)
#获取张量的维度数
print(tensor_3d.dim())
#是否启用梯度计算
print(tensor_3d.requires_grad)
#获取张量中的元素总数
print(tensor_3d.numel())
print(tensor_3d.is_cuda)
print(tensor_3d.T)
#检查张量是否连续存储
print(tensor_3d.is_contiguous())'''

'''#张量的操作
# 创建一个 2D 张量
tensor = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
print("原始张量:\n", tensor)

# 1. **索引和切片操作**
print("\n【索引和切片】")
print("获取第一行:", tensor[0])  # 获取第一行
print("获取第一行第一列的元素:", tensor[0, 0])  # 获取特定元素
print("获取第二列的所有元素:", tensor[:, 1])  # 获取第二列所有元素

# 2. **形状变换操作**
print("\n【形状变换】")
reshaped = tensor.view(3, 2)  # 改变张量形状为 3x2
print("改变形状后的张量:\n", reshaped)
flattened = tensor.flatten()  # 将张量展平成一维
print("展平后的张量:\n", flattened)

# 3. **数学运算操作**
print("\n【数学运算】")
tensor_add = tensor + 10  # 张量加法
print("张量加 10:\n", tensor_add)
tensor_mul = tensor * 2  # 张量乘法
print("张量乘 2:\n", tensor_mul)
tensor_sum = tensor.sum()  # 计算所有元素的和
print("张量元素的和:", tensor_sum.item())

# 4. **与其他张量的操作**
print("\n【与其他张量操作】")
tensor2 = torch.tensor([[1, 1, 1], [1, 1, 1]], dtype=torch.float32)
print("另一个张量:\n", tensor2)
tensor_dot = torch.matmul(tensor, tensor2.T)  # 张量矩阵乘法
print("矩阵乘法结果:\n", tensor_dot)

# 5. **条件判断和筛选**
print("\n【条件判断和筛选】")
mask = tensor > 3  # 创建一个布尔掩码
print("大于 3 的元素的布尔掩码:\n", mask)
filtered_tensor = tensor[tensor > 3]  # 筛选出符合条件的元素
print("大于 3 的元素:\n", filtered_tensor)'''

data = torch.randn(100, 2)
print(data)
labels1 = (data[:, 0] ** 2 + data[:, 1] ** 2 < 1).float()
print(labels1)
labels = labels1.unsqueeze(1)  # 点在圆内为1，圆外为0
print(labels)

# 可视化数据
plt.scatter(data[:, 0], data[:, 1], c=labels.squeeze(), cmap='coolwarm')
plt.title("Generated Data")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
