import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
diesel_loco = np.array([0.907, 0.878, 0.848, 0.81, 0.80, 0.80, 0.78, 0.78, 0.78, 0.78])
electric_loco = np.array([1.193, 1.222, 1.252, 1.29, 1.37, 1.38, 1.39, 1.42, 1.46, 1.47])
electric_loco_pct = np.array([56.8, 58.1, 59.5, 61.3, 63.0, 62.7, 63.8, 63.3, 65.2, 65.3])

# 创建图形
fig, ax1 = plt.subplots(figsize=(12, 6))

# 绘制柱状图 (机车拥有量)
bar_width = 0.4
x = np.arange(len(years))
bars1 = ax1.bar(x - bar_width/2, diesel_loco, bar_width, label='内燃机车 (万台)', color='skyblue', alpha=0.8)
bars2 = ax1.bar(x + bar_width/2, electric_loco, bar_width, label='电力机车 (万台)', color='lightgreen', alpha=0.8)

# 设置左侧Y轴
ax1.set_xlabel('年份')
ax1.set_ylabel('拥有量 (万台)')
ax1.set_title('2015-2024年全国铁路机车拥有量及电力机车占比变化')
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(loc='upper left')

# 创建右侧Y轴
ax2 = ax1.twinx()
line1, = ax2.plot(x, electric_loco_pct, 'ro-', linewidth=2, label='电力机车占比 (%)')
ax2.set_ylabel('占比 (%)')
ax2.set_ylim(30, 70)  # 调整范围以适应折线

# 添加图例
lines, labels = ax2.get_legend_handles_labels()
ax1.legend(lines + ax1.get_legend_handles_labels()[0], labels + ax1.get_legend_handles_labels()[1], loc='upper right')

plt.tight_layout()
plt.show()