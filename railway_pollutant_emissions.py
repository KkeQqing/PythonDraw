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

# 绘制面积图 (化学需氧量)
# 修改了颜色和透明度
ax1.fill_between(years, cod_emission, alpha=0.5, color='#20B2AA', label='化学需氧量 (吨)')
ax1.set_xlabel('年份')
ax1.set_ylabel('化学需氧量 (吨)')
ax1.set_title('2015-2024年铁路主要污染物排放量变化')
ax1.legend(loc='upper left')

# 创建右侧Y轴 (二氧化硫)
ax2 = ax1.twinx()
ax2.plot(years, so2_emission, 'r-o', label='二氧化硫 (吨)', linewidth=2)
ax2.set_ylabel('二氧化硫 (吨)')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()