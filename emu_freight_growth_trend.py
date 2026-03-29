import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
emu_groups = np.array([1883, 2586, 2935, 3256, 3665, 3918, 4153, 4194, 4427, 4806])
freight_cars = np.array([72.3, 76.4, 79.9, 83.0, 87.8, 91.2, 96.6, 99.7, 100.7, 101.9])

# 创建图形
plt.figure(figsize=(12, 6))

# 绘制动车组 (折线)
plt.plot(years, emu_groups, 'b-o', label='动车组 (标准组)', linewidth=2, markersize=6)

# 绘制货车 (折线)
# 注意：为了在同一张图上对比趋势，这里将货车数据缩小了10倍（除以10）以匹配动车组的数值范围
# 实际趋势是同步增长的，只是绝对数值量级不同。
plt.plot(years, freight_cars * 10, 'r-x', label='货车 (万辆) * 10', linewidth=2, markersize=6)

plt.title('2015-2024年动车组与货车拥有量增长趋势')
plt.xlabel('年份')
plt.ylabel('拥有量')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()