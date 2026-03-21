import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================
# 1. 数据准备
# ==========================
days = ['一', '二', '三', '四', '五', '六', '日']
screen_on = [16.2, 13.3, 15.9, 15.5, 11.6, 15.1, 14.7]
screen_off = [0.5, 0.3, 0.6, 0.4, 0.9, 0.9, 0.7]
total_time = [s + o for s, o in zip(screen_on, screen_off)]

categories = ['游戏', '工具', '阅读', '社交', '其他']
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
# 2. 生成左侧热点图颜色 (核心逻辑 - 已加深)
# ==========================
def get_heat_color(value, min_val, max_val, color_type):
    if max_val == min_val:
        return "rgb(240, 240, 240)"
    norm = (value - min_val) / (max_val - min_val)

    # 橙色系 (熄屏)
    if color_type == 'orange':
        r = 255
        g = int(255 - (255 - 69) * norm)
        b = int(200 - (200 - 0) * norm)
        return f"rgb({r}, {g}, {b})"
    # 绿色系 (总时长)
    elif color_type == 'green':
        r = int(220 - (220 - 0) * norm)
        g = int(255 - (255 - 100) * norm)
        b = int(220 - (220 - 0) * norm)
        return f"rgb({r}, {g}, {b})"
    # 蓝色系 (亮屏时长)
    elif color_type == 'blue':
        r = int(200 - (200 - 0) * norm)
        g = int(230 - (230 - 50) * norm)
        b = int(255 - (255 - 150) * norm)
        return f"rgb({r}, {g}, {b})"
    # 黄色系 (游戏)
    elif color_type == 'yellow':
        r = 255
        g = int(255 - (255 - 180) * norm)  # 稍微加深中间调
        b = int(200 - (200 - 0) * norm)
        return f"rgb({r}, {g}, {b})"

    # 【修改点】工具类：深森林绿 (Deep Forest Green)
    # 浅绿 (144, 238, 144) -> 深绿 (0, 100, 0)
    elif color_type == 'tool_green':
        r = int(144 - (144 - 0) * norm)
        g = int(238 - (238 - 100) * norm)
        b = int(144 - (144 - 0) * norm)
        return f"rgb({r}, {g}, {b})"

    # 橙红色系 (阅读)
    elif color_type == 'read_red':
        r = 255
        g = int(200 - (200 - 50) * norm)
        b = int(200 - (200 - 50) * norm)
        return f"rgb({r}, {g}, {b})"
    # 紫色系 (社交)
    elif color_type == 'social_purple':
        r = int(200 - (200 - 100) * norm)
        g = int(200 - (200 - 0) * norm)
        b = int(255 - (255 - 200) * norm)
        return f"rgb({r}, {g}, {b})"

    # 【修改点】其他类：深宝蓝色 (Deep Royal Blue)
    # 浅蓝 (135, 206, 250) -> 深蓝 (0, 0, 139)
    elif color_type == 'other_blue':
        r = int(135 - (135 - 0) * norm)
        g = int(206 - (206 - 0) * norm)
        b = int(250 - (250 - 139) * norm)
        return f"rgb({r}, {g}, {b})"

    return "rgb(240, 240, 240)"


# 计算归一化范围
min_off, max_off = min(screen_off), max(screen_off)
min_on, max_on = min(screen_on), max(screen_on)
min_tot, max_tot = min(total_time), max(total_time)

# 提取各列数据
col_game = [p[0] for p in percentages]
col_tool = [p[1] for p in percentages]
col_read = [p[2] for p in percentages]
col_social = [p[3] for p in percentages]
col_other = [p[4] for p in percentages]

# 生成所有列的颜色列表
colors_day = ['rgba(245, 245, 245, 1)'] * len(days)
colors_off = [get_heat_color(v, min_off, max_off, 'orange') for v in screen_off]
colors_on = [get_heat_color(v, min_on, max_on, 'blue') for v in screen_on]
colors_tot = [get_heat_color(v, min_tot, max_tot, 'green') for v in total_time]

# 应用类别颜色 (百分比 0-100 归一化)
colors_game = [get_heat_color(v, 0, 100, 'yellow') for v in col_game]
colors_tool = [get_heat_color(v, 0, 100, 'tool_green') for v in col_tool]  # 新深绿色
colors_read = [get_heat_color(v, 0, 100, 'read_red') for v in col_read]
colors_social = [get_heat_color(v, 0, 100, 'social_purple') for v in col_social]
colors_other = [get_heat_color(v, 0, 100, 'other_blue') for v in col_other]  # 新深蓝色

cells_values = [
    [f"{d}" for d in days],
    [f"{v:.1f}" for v in screen_off],
    [f"{v:.1f}" for v in screen_on],
    [f"{v:.1f}" for v in total_time],
    [f"{v}%" for v in col_game],
    [f"{v}%" for v in col_tool],
    [f"{v}%" for v in col_read],
    [f"{v}%" for v in col_social],
    [f"{v}%" for v in col_other]
]

cells_colors = [
    colors_day,
    colors_off,
    colors_on,
    colors_tot,
    colors_game,
    colors_tool,
    colors_read,
    colors_social,
    colors_other
]

# ==========================
# 3. 构建桑基图数据
# ==========================
node_labels = [f"{d} {total_time[i]:.1f}h" for i, d in enumerate(days)] + categories

# 定义右侧类别的基础 RGB 值 (用于混合计算 - 已同步加深)
cat_base_rgb = [
    [255, 215, 0],  # 游戏
    [0, 100, 0],  # 工具 (深绿)
    [255, 69, 0],  # 阅读
    [148, 0, 211],  # 社交
    [0, 0, 139]  # 其他 (深蓝)
]

# 计算左侧星期节点的混合颜色
day_node_colors = []
for i in range(len(days)):
    r_sum, g_sum, b_sum = 0, 0, 0

    for j in range(len(categories)):
        weight = percentages[i][j] / 100.0
        base_r, base_g, base_b = cat_base_rgb[j]

        r_sum += base_r * weight
        g_sum += base_g * weight
        b_sum += base_b * weight

    # 混合后稍微提亮一点，防止混合后太黑，但保持饱和度
    final_r = int(min(255, r_sum * 1.1))
    final_g = int(min(255, g_sum * 1.1))
    final_b = int(min(255, b_sum * 1.1))

    day_node_colors.append(f"rgb({final_r}, {final_g}, {final_b})")

# 组合所有节点颜色 (右侧节点颜色也加深)
node_colors = day_node_colors + ['#FFD700', '#006400', '#FF4500', '#9400D3', '#00008B']

sources = []
targets = []
values = []
link_colors = []
link_labels = []

# 连线颜色 (半透明但底色更深)
cat_colors_rgba = [
    'rgba(255, 215, 0, 0.7)',
    'rgba(0, 100, 0, 0.7)',  # 深绿连线
    'rgba(255, 69, 0, 0.7)',
    'rgba(148, 0, 211, 0.7)',
    'rgba(0, 0, 139, 0.7)'  # 深蓝连线
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
# 4. 绘图
# ==========================
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'table'}, {'type': 'sankey'}]],
    column_widths=[0.45, 0.55],
    horizontal_spacing=0.02
)

# --- 左侧表格 ---
fig.add_trace(
    go.Table(
        header=dict(
            values=['<b>星期</b>', '<b>熄屏</b>', '<b>亮屏</b>', '<b>总时长</b>',
                    '<b>游戏</b>', '<b>工具</b>', '<b>阅读</b>', '<b>社交</b>', '<b>其他</b>'],
            fill_color='#FAFAFA',
            align='center',
            font=dict(color='black', size=12),
            height=35
        ),
        cells=dict(
            values=cells_values,
            fill_color=cells_colors,
            align='center',
            font=dict(color='black', size=11),
            height=35
        )
    ),
    row=1, col=1
)

# --- 右侧桑基图 ---
fig.add_trace(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=1),
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            label=link_labels
        )
    ),
    row=1, col=2
)

fig.update_layout(
    title_text="<b>每周屏幕活动全览</b>",
    font=dict(family="Arial", size=11, color="black"),
    height=750,
    margin=dict(l=10, r=10, t=60, b=10),
    showlegend=False,
    uniformtext=dict(mode='show', minsize=9)
)

fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)

fig.show()