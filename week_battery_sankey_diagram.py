import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================
# 1. 数据准备
# ==========================
days = ['一', '二', '三', '四', '五', '六', '日']
screen_on = [16.2, 13.3, 15.9, 15.5, 11.6, 15.1, 14.7]
screen_off = [0.5, 0.3, 0.6, 0.4, 0.9, 0.9, 0.7]
total_time = [s + o for s, o in zip(screen_on, screen_off)]

categories = ['游戏娱乐', '工具类', '阅读类', '社交沟通', '其他']
percentages = [
    [21, 23, 14, 39, 3],  # 一
    [35, 18, 29, 13, 5],  # 二
    [32, 6, 58, 3, 1],  # 三
    [42, 3, 21, 31, 3],  # 四
    [53, 6, 3, 29, 9],  # 五
    [75, 1, 2, 20, 2],  # 六
    [18, 8, 51, 20, 3]  # 日
]

# 计算流量值
flow_values = []
for i in range(len(days)):
    day_flows = []
    for j in range(len(categories)):
        val = total_time[i] * (percentages[i][j] / 100.0)
        day_flows.append(val)
    flow_values.append(day_flows)


# ==========================
# 2. 生成左侧热点图颜色
# ==========================
def get_heat_color(value, min_val, max_val, color_type):
    if max_val == min_val:
        return "rgb(240, 240, 240)"
    norm = (value - min_val) / (max_val - min_val)

    if color_type == 'orange':
        # 橙色系：浅黄 -> 深橙红
        r = 255
        g = int(255 - (255 - 69) * norm)
        b = int(200 - (200 - 0) * norm)
        return f"rgb({r}, {g}, {b})"
    elif color_type == 'green':
        # 绿色系：浅绿 -> 深绿
        r = int(220 - (220 - 0) * norm)
        g = int(255 - (255 - 100) * norm)
        b = int(220 - (220 - 0) * norm)
        return f"rgb({r}, {g}, {b})"
    return "rgb(240, 240, 240)"


min_off, max_off = min(screen_off), max(screen_off)
min_tot, max_tot = min(total_time), max(total_time)

colors_off = [get_heat_color(v, min_off, max_off, 'orange') for v in screen_off]
colors_tot = [get_heat_color(v, min_tot, max_tot, 'green') for v in total_time]
colors_day = ['rgba(245, 245, 245, 1)'] * len(days)
colors_on = ['rgba(255, 255, 255, 1)'] * len(days)

cells_values = [
    [f"{d}" for d in days],
    [f"{v:.1f}" for v in screen_off],
    [f"{v:.1f}" for v in screen_on],
    [f"{v:.1f}" for v in total_time]
]

cells_colors = [
    colors_day,
    colors_off,
    colors_on,
    colors_tot
]

# ==========================
# 3. 构建桑基图数据
# ==========================
node_labels = days + categories

# 右侧节点高饱和度颜色
cat_colors_hex = ['#FFD700', '#00FF7F', '#FF4500', '#9400D3', '#607D8B']
# 左侧节点统一淡色
node_colors = ['#E3F2FD'] * len(days) + cat_colors_hex

sources = []
targets = []
values = []
link_colors = []
link_labels = []

cat_colors_rgba = [
    'rgba(255, 215, 0, 0.6)',  # 游戏
    'rgba(0, 255, 127, 0.6)',  # 工具
    'rgba(255, 69, 0, 0.6)',  # 阅读
    'rgba(148, 0, 211, 0.6)',  # 社交
    'rgba(96, 125, 139, 0.6)'  # 其他
]

for i in range(len(days)):
    for j in range(len(categories)):
        val = flow_values[i][j]
        if val > 0.01:
            sources.append(i)
            targets.append(len(days) + j)
            values.append(val)
            link_colors.append(cat_colors_rgba[j])
            link_labels.append(f"{val:.1f}h")

        # ==========================
# 4. 绘图 (兼容旧版 Plotly)
# ==========================
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'table'}, {'type': 'sankey'}]],
    column_widths=[0.35, 0.65],
    horizontal_spacing=0.02
)

# --- 左侧表格 ---
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
            values=cells_values,
            fill_color=cells_colors,
            align='center',
            font=dict(color='black', size=13),
            height=40
        )
    ),
    row=1, col=1
)

# --- 右侧桑基图 (已移除所有内部 font 属性) ---
fig.add_trace(
    go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="black", width=1),
            label=node_labels,
            color=node_colors
            # 注意：这里完全移除了 font 属性
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            label=link_labels
            # 注意：这里完全移除了 font 属性
        )
    ),
    row=1, col=2
)

# --- 关键修复：在 layout 层级统一设置字体 ---
fig.update_layout(
    title_text="<b>每周屏幕活动分析：左侧热点图 (熄屏橙/总长绿) + 右侧流向桑基图</b>",
    # 全局字体设置，这将同时作用于桑基图的节点文字和连线标签
    font=dict(family="Arial", size=12, color="black"),
    height=700,
    margin=dict(l=10, r=10, t=60, b=10),
    showlegend=False,
    # 强制显示连线标签，并设置最小字号，解决文字不显示或太小的问题
    uniformtext=dict(mode='show', minsize=10)
)

# 隐藏坐标轴
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)

fig.show()