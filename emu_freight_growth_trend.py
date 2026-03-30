import matplotlib.pyplot as plt
import numpy as np

# 1. 设置中文字体 (防止乱码)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 2. 准备数据
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
emu_groups = np.array([1883, 2586, 2935, 3256, 3665, 3918, 4153, 4194, 4427, 4806])
freight_cars = np.array([72.3, 76.4, 79.9, 83.0, 87.8, 91.2, 96.6, 99.7, 100.7, 101.9])

# 3. 创建图形
plt.figure(figsize=(12, 6))

# --- 绘制动车组 (折线) ---
# 这里的绘图数据是原始数据
plt.plot(years, emu_groups, 'b-o', label='动车组 (标准组)', linewidth=2, markersize=6)

# --- 绘制货车 (折线) ---
# 绘图时放大了10倍，为了让数值范围匹配，但标注时要还原
plt.plot(years, freight_cars * 10, 'r-x', label='货车 (万辆) * 10', linewidth=2, markersize=6)

# --- 核心修改：添加数值标注 ---

# 1. 标注动车组数据
# zip函数可以将年份、动车组数量两个列表打包，方便同时遍历
for x, y in zip(years, emu_groups):
    # plt.text(x坐标, y坐标, '显示的文本', 对齐方式, 偏移量)
    plt.text(x, y + 50, f'{y}', ha='center', va='bottom', fontsize=9, color='blue')

# 2. 标注货车数据
for x, y in zip(years, freight_cars):
    # 注意：y在这里是原始数据(如72.3)，但图上画的位置是 y*10
    # 所以垂直位置设为 y*10 + 50，显示的文本直接用 f'{y}'
    plt.text(x, y * 10 + 50, f'{y}', ha='center', va='bottom', fontsize=9, color='red')

# 4. 图表装饰
plt.title('2015-2024年动车组与货车拥有量增长趋势')
plt.xlabel('年份')
plt.ylabel('拥有量 (单位：标准组/万辆)') # 修改Y轴标签以更准确
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()