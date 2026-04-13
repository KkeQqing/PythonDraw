# 导入数据处理和绘图的基础库
# 请补全以下常用库的导入语句
import pandas as pd  # 用于数据处理
import numpy as np  # 用于数值计算
import matplotlib.pyplot as plt  # 用于绘图

# 加载数据集
# 请读取当前目录下的 electric_vehicle_driverange.csv 文件，并保存到变量 data 中。使用 pandas.read_csv() 函数来加载数据。
data= pd.read_csv("electric_vehicle_driverange.csv")

# 查看数据集的前几行，确保数据已正确加载
data.head()