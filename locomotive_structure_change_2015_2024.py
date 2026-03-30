import matplotlib.pyplot as plt
import numpy as np

# 1. 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 2. 数据准备
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
diesel_loco = np.array([0.907, 0.878, 0.848, 0.81, 0.80, 0.80, 0.78, 0.78, 0.78, 0.78])
electric_loco = np.array([1.193, 1.222, 1.252, 1.29, 1.37, 1.38, 1.39, 1.42, 1.46, 1.47])
electric_loco_pct = np.array([56.8, 58.1, 59.5, 61.3, 63.0, 62.7, 63.8, 63.3, 65.2, 65.3])

# 3. 创建图形
fig, ax1 = plt.subplots(figsize=(12, 6))

# --- 绘制柱状图 (机车拥有量) ---
bar_width = 0.4
x = np.arange(len(years))
bars1 = ax1.bar(x - bar_width/2, diesel_loco, bar_width, label='内燃机车 (万台)', color='skyblue', alpha=0.8)
bars2 = ax1.bar(x + bar_width/2, electric_loco, bar_width, label='电力机车 (万台)', color='lightgreen', alpha=0.8)

# --- 核心修改：为柱状图添加数值标签 ---
def add_labels(bars, axis):
    """辅助函数：在柱子顶部显示数值"""
    for bar in bars:
        height = bar.get_height()
        axis.text(bar.get_x() + bar.get_width() / 2, height + 0.02,  # 0.02是微小偏移量，防止贴在柱子上
                  f'{height:.3f}',  # 格式化为3位小数
                  ha='center', va='bottom', fontsize=9)

add_labels(bars1, ax1)
add_labels(bars2, ax1)

# 设置左侧Y轴
ax1.set_xlabel('年份')
ax1.set_ylabel('拥有量 (万台)')
ax1.set_title('2015-2024年全国铁路机车拥有量及电力机车占比变化')
ax1.set_xticks(x)
ax1.set_xticklabels(years)

# --- 创建右侧Y轴并绘制折线图 ---
ax2 = ax1.twinx()
line1, = ax2.plot(x, electric_loco_pct, 'ro-', linewidth=2, label='电力机车占比 (%)', markersize=6)

# --- 核心修改：为折线图添加数值标签 ---
for i, v in enumerate(electric_loco_pct):
    ax2.text(i, v + 0.5, f'{v:.1f}%',  # +0.5 是微小偏移量，防止贴在点上；格式化为 1 位小数加%
             ha='center', va='bottom', color='red', fontsize=9)

# 设置右侧Y轴范围，避免折线与柱状图重叠
ax2.set_ylabel('占比 (%)')
ax2.set_ylim(45, 70)  # 根据数据调整，确保 56.8% 的起点有空间显示

# --- 合并图例 ---
# 获取两个轴的图例句柄和标签
lines, labels = ax2.get_legend_handles_labels()
bars, bar_labels = ax1.get_legend_handles_labels()
# 合并并在左上角显示
ax1.legend(bars + lines, bar_labels + labels, loc='upper left')

plt.tight_layout()
plt.show()