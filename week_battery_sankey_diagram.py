import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ==========================
# 1. 数据准备与处理
# ==========================

# 基础数据
days = ['一', '二', '三', '四', '五', '六', '日']
screen_on = [16.2, 13.3, 15.9, 15.5, 11.6, 15.1, 14.7]
screen_off = [0.5, 0.3, 0.6, 0.4, 0.9, 0.9, 0.7]
total_time = [s + o for s, o in zip(screen_on, screen_off)]

# 应用类别
categories = ['游戏娱乐', '工具类', '阅读类', '社交沟通', '其他']

# 百分比数据 (按行：星期一到星期日)
# 格式: [游戏, 工具, 阅读, 社交, 其他]
percentages = [
    [21, 23, 14, 39, 3],  # 一
    [35, 18, 29, 13, 5],  # 二
    [32, 6, 58, 3, 1],  # 三
    [42, 3, 21, 31, 3],  # 四
    [53, 6, 3, 29, 9],  # 五
    [75, 1, 2, 20, 2],  # 六
    [18, 8, 51, 20, 3]  # 日
]

# 计算具体时长 (流量值)
# flow_values[天索引][类别索引] = 时长
flow_values = []
for i in range(len(days)):
    day_flows = []
    for j in range(len(categories)):
        # 总时长 * 百分比
        val = total_time[i] * (percentages[i][j] / 100.0)
        day_flows.append(val)
    flow_values.append(day_flows)

# ==========================
# 2. 构建桑基图数据 (右侧)
# ==========================

# 节点定义
# 索引 0-6: 星期 (一 ~ 日)
# 索引 7-11: 应用类别 (游戏 ~ 其他)
node_labels = days + categories
node_colors = ['#4DA6FF'] * len(days) + ['#FFD700', '#98FB98', '#FFA07A', '#DDA0DD', '#D3D3D3']
# 星期用蓝色系，类别用不同区分色

# 连线数据
sources = []
targets = []
values = []
link_colors = []

# 为每个类别定义一个基准色，用于连线，使流向更清晰
cat_base_colors = [
    'rgba(255, 215, 0, 0.4)',  # 游戏
    'rgba(152, 251, 152, 0.4)',  # 工具
    'rgba(255, 160, 122, 0.4)',  # 阅读
    'rgba(221, 160, 221, 0.4)',  # 社交
    'rgba(211, 211, 211, 0.4)'  # 其他
]

for i, day in enumerate(days):
    src_idx = i  # 星期节点索引
    for j, cat in enumerate(categories):
        tgt_idx = len(days) + j  # 类别节点索引
        val = flow_values[i][j]

        if val > 0.05:  # 忽略极小值
            sources.append(src_idx)
            targets.append(tgt_idx)
            values.append(val)
            link_colors.append(cat_base_colors[j])


# ==========================
# 3. 构建左侧表格数据 (热点图样式)
# ==========================

# 为了制造热点图效果，我们需要根据数值大小生成颜色深浅
def get_heatmap_color(value, max_val, min_val, color_scale='Blues'):
    # 简单的线性插值生成颜色透明度或亮度，这里使用 Plotly 内置色阶逻辑模拟
    # 归一化 0-1
    if max_val == min_val: return "rgb(240,240,240)"
    norm = (value - min_val) / (max_val - min_val)

    # 这里手动模拟一个蓝色系的热点渐变 (浅蓝 -> 深蓝)
    # 基础色: 200, 230, 255 (很浅)
    # 深色: 0, 100, 200 (深)
    r = int(200 - norm * 200)
    g = int(230 - norm * 130)
    b = int(255 - norm * 55)
    return f"rgb({r},{g},{b})"


# 计算各列的最大最小值用于归一化
max_on, min_on = max(screen_on), min(screen_on)
max_off, min_off = max(screen_off), min(screen_off)
max_tot, min_tot = max(total_time), min(total_time)

# 生成表格单元格的颜色背景
colors_on = [get_heatmap_color(v, max_on, min_on) for v in screen_on]
colors_off = [get_heatmap_color(v, max_off, min_off) for v in screen_off]
colors_tot = [get_heatmap_color(v, max_tot, min_tot) for v in total_time]
# 星期列背景色固定
colors_day = ['rgba(240,248,255,0.8)'] * len(days)

# 表格内容 (添加单位)
cells_data = [
    [f"{d} " for d in days],
    [f"{v:.1f}" for v in screen_off],
    [f"{v:.1f}" for v in screen_on],
    [f"{v:.1f}" for v in total_time]
]

cell_colors = [
    colors_day,
    colors_off,
    colors_on,
    colors_tot
]

# ==========================
# 4. 绘制组合图
# ==========================

# 创建子图：左侧是表格 (domain)，右侧是桑基图 (domain)
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'table'}, {'type': 'sankey'}]],
    horizontal_spacing=0.02,  # 间距很小，营造连接感
    column_widths=[0.35, 0.65]  # 左侧表格窄一点，右侧桑基图宽一点
)

# --- 添加左侧表格 ---
fig.add_trace(
    go.Table(
        header=dict(
            values=['<b>星期</b>', '<b>熄屏时长</b>', '<b>亮屏时长</b>', '<b>总时长</b>'],
            fill_color='#FAFAFA',
            align='center',
            font=dict(color='black', size=14),
            height=40
        ),
        cells=dict(
            values=cells_data,
            fill_color=cell_colors,
            align='center',
            font=dict(color='black', size=13),
            height=40
        ),
        columnwidth=[50, 80, 80, 80]
    ),
    row=1, col=1
)

# --- 添加右侧桑基图 ---
fig.add_trace(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors,
            x=[0.1] * len(days) + [0.9] * len(categories),  # 强制节点位置：左边是星期，右边是类别
            y=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7] + [0.1, 0.3, 0.5, 0.7, 0.9]  # 简单分布，Plotly会自动调整优化
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate='从 %{source.label} 到 %{target.label}<br>时长: %{value:.2f} 小时<extra></extra>'
        )
    ),
    row=1, col=2
)

# 更新布局
fig.update_layout(
    title_text="<b>每周屏幕活动时长分布与应用类别流向桑基图</b>",
    font_size=12,
    height=700,
    margin=dict(l=10, r=10, t=60, b=10),
    showlegend=False
)

# 隐藏坐标轴
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)

# 显示图表
fig.show()

# 如果需要保存为HTML
# fig.write_html("screen_activity_sankey.html")