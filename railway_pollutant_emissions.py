import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
cod_emission = np.array([2002, 1965, 1901, 1878, 1764, 1634, 1611, 1448, 1466, 1337])
so2_emission = np.array([28760, 23924, 15817, 9836, 5438, 3271, 2000, 1228, 652, 456])

# 创建图形
fig, ax1 = plt.subplots(figsize=(12, 6))

# --- 绘制面积图 (化学需氧量) ---
# 使用 alpha 控制透明度以便看清背景网格和数值
ax1.fill_between(years, cod_emission, alpha=0.5, color='#20B2AA', label='化学需氧量 (吨)')

# --- 绘制折线图 (二氧化硫) ---
# 注意：由于二氧化硫数值远大于化学需氧量，必须使用双Y轴
ax2 = ax1.twinx()
line, = ax2.plot(years, so2_emission, 'r-o', label='二氧化硫 (吨)', linewidth=2)

# --- 设置坐标轴标签和标题 ---
ax1.set_xlabel('年份')
ax1.set_ylabel('化学需氧量 (吨)')
ax2.set_ylabel('二氧化硫 (吨)')
ax1.set_title('2015-2024年铁路主要污染物排放量变化')

# --- 核心修改：添加数值标注 ---

# 1. 标注折线图 (二氧化硫) 的数值
# 为了防止遮挡，y坐标稍微向上偏移 (0.05)
for i, (x, y) in enumerate(zip(years, so2_emission)):
    ax2.text(x, y + 0.05 * y, f'{int(y)}', ha='center', va='bottom', color='r', fontsize=10)

# 2. 标注面积图 (化学需氧量) 的关键数值 (起始点和结束点)
# 起始点 (2015年)
ax1.text(years[0], cod_emission[0], f'{cod_emission[0]}', ha='center', va='bottom', color='black', fontsize=10)
# 结束点 (2024年)
ax1.text(years[-1], cod_emission[-1], f'{cod_emission[-1]}', ha='center', va='bottom', color='black', fontsize=10)

# --- 设置图例位置 ---
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.tight_layout()
plt.show()