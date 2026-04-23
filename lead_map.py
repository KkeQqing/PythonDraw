import math
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context


# =========================
# 1) 原始数据
# =========================
raw_data = [
    {"国家": "澳大利亚", "姓名": "托尼·阿博特", "出生年份": 1957, "学历": "理科", "任期年数": 2.0, "进入政坛年份": 1994, "当选领导人年份": 2013, "进入政坛年龄": 37, "当选领导人年龄": 56, "多久当选领导人": 19, "政治路线": "右翼"},
    {"国家": "奥地利", "姓名": "维尔纳·法伊曼", "出生年份": 1960, "学历": "辍学/无", "任期年数": 7.0, "进入政坛年份": 1989, "当选领导人年份": 2008, "进入政坛年龄": 29, "当选领导人年龄": 48, "多久当选领导人": 19, "政治路线": "左翼"},
    {"国家": "巴西", "姓名": "迪尔玛·罗塞夫", "出生年份": 1947, "学历": "理科", "任期年数": 5.0, "进入政坛年份": 1981, "当选领导人年份": 2011, "进入政坛年龄": 34, "当选领导人年龄": 64, "多久当选领导人": 30, "政治路线": "左翼"},
    {"国家": "加拿大", "姓名": "史蒂芬·哈珀", "出生年份": 1959, "学历": "理科", "任期年数": 9.0, "进入政坛年份": 1993, "当选领导人年份": 2006, "进入政坛年龄": 34, "当选领导人年龄": 47, "多久当选领导人": 13, "政治路线": "右翼"},
    {"国家": "丹麦", "姓名": "赫勒·托宁-施密特", "出生年份": 1966, "学历": "艺术/理科", "任期年数": 4.0, "进入政坛年份": 1988, "当选领导人年份": 2011, "进入政坛年龄": 22, "当选领导人年龄": 45, "多久当选领导人": 23, "政治路线": "左翼"},
    {"国家": "芬兰", "姓名": "于尔基·卡泰宁", "出生年份": 1971, "学历": "法律", "任期年数": 3.0, "进入政坛年份": 1999, "当选领导人年份": 2011, "进入政坛年龄": 28, "当选领导人年龄": 40, "多久当选领导人": 12, "政治路线": "右翼"},
    {"国家": "法国", "姓名": "弗朗索瓦·奥朗德", "出生年份": 1954, "学历": "商业/理科", "任期年数": 5.0, "进入政坛年份": 1983, "当选领导人年份": 2012, "进入政坛年龄": 29, "当选领导人年龄": 58, "多久当选领导人": 29, "政治路线": "左翼"},
    {"国家": "格鲁吉亚", "姓名": "伊拉克利·加里巴什维利", "学历": "艺术", "出生年份": 1982, "任期年数": 5.0, "进入政坛年份": 2011, "当选领导人年份": 2013, "进入政坛年龄": 29, "当选领导人年龄": 31, "多久当选领导人": 2, "政治路线": "右翼"},
    {"国家": "德国", "姓名": "安格拉·默克尔", "出生年份": 1954, "学历": "理科", "任期年数": 16.0, "进入政坛年份": 1990, "当选领导人年份": 2005, "进入政坛年龄": 36, "当选领导人年龄": 51, "多久当选领导人": 15, "政治路线": "中间"},
    {"国家": "希腊", "姓名": "安东尼斯·萨马拉斯", "出生年份": 1951, "学历": "理科", "任期年数": 2.5, "进入政坛年份": 1993, "当选领导人年份": 2012, "进入政坛年龄": 42, "当选领导人年龄": 61, "多久当选领导人": 19, "政治路线": "右翼"},
    {"国家": "巴巴多斯", "姓名": "艾蕾卡·哈蒙德", "出生年份": 1965, "学历": "辍学/无", "任期年数": 1.5, "进入政坛年份": 2005, "当选领导人年份": 2013, "进入政坛年龄": 40, "当选领导人年龄": 48, "多久当选领导人": 8, "政治路线": "左翼"},
    {"国家": "印度", "姓名": "曼莫汉·辛格", "出生年份": 1932, "学历": "理科", "任期年数": 10.0, "进入政坛年份": 1991, "当选领导人年份": 2004, "进入政坛年龄": 59, "当选领导人年龄": 72, "多久当选领导人": 13, "政治路线": "中间"},
    {"国家": "伊拉克", "姓名": "努里·马利基", "出生年份": 1950, "学历": "艺术", "任期年数": 8.0, "进入政坛年份": 2005, "当选领导人年份": 2006, "进入政坛年龄": 55, "当选领导人年龄": 56, "多久当选领导人": 1, "政治路线": "左翼"},
    {"国家": "爱尔兰", "姓名": "恩达·肯尼", "出生年份": 1951, "学历": "不明", "任期年数": 6.0, "进入政坛年份": 1975, "当选领导人年份": 2011, "进入政坛年龄": 24, "当选领导人年龄": 60, "多久当选领导人": 36, "政治路线": "中间"},
    {"国家": "以色列", "姓名": "本杰明·内塔尼亚胡", "出生年份": 1949, "学历": "艺术/商业/理科", "任期年数": 16.0, "进入政坛年份": 1988, "当选领导人年份": 2009, "进入政坛年龄": 39, "当选领导人年龄": 60, "多久当选领导人": 21, "政治路线": "右翼"},
    {"国家": "意大利", "姓名": "马泰奥·伦齐", "出生年份": 1975, "学历": "法律", "任期年数": 2.0, "进入政坛年份": 2006, "当选领导人年份": 2014, "进入政坛年龄": 31, "当选领导人年龄": 39, "多久当选领导人": 8, "政治路线": "中间"},
    {"国家": "日本", "姓名": "安倍晋三", "出生年份": 1954, "学历": "理科", "任期年数": 8.0, "进入政坛年份": 1977, "当选领导人年份": 2012, "进入政坛年龄": 23, "当选领导人年龄": 58, "多久当选领导人": 35, "政治路线": "右翼"},
    {"国家": "朝鲜", "姓名": "朴凤柱", "出生年份": 1939, "学历": "辍学/无", "任期年数": 6.0, "进入政坛年份": 1980, "当选领导人年份": 2013, "进入政坛年龄": 41, "当选领导人年龄": 74, "多久当选领导人": 33, "政治路线": "右翼"},
    {"国家": "韩国", "姓名": "郑烘原", "出生年份": 1944, "学历": "法律", "任期年数": 2.0, "进入政坛年份": 2004, "当选领导人年份": 2013, "进入政坛年龄": 60, "当选领导人年龄": 69, "多久当选领导人": 9, "政治路线": "右翼"},
    {"国家": "卢森堡", "姓名": "格扎维埃·贝泰尔", "出生年份": 1973, "学历": "法律/理科", "任期年数": 10.0, "进入政坛年份": 2011, "当选领导人年份": 2013, "进入政坛年龄": 38, "当选领导人年龄": 40, "多久当选领导人": 2, "政治路线": "中间"},
    {"国家": "荷兰", "姓名": "马克·吕特", "出生年份": 1967, "学历": "历史", "任期年数": 14.0, "进入政坛年份": 2002, "当选领导人年份": 2010, "进入政坛年龄": 35, "当选领导人年龄": 43, "多久当选领导人": 8, "政治路线": "中间"},
    {"国家": "新西兰", "姓名": "约翰·基", "出生年份": 1961, "学历": "商业", "任期年数": 8.0, "进入政坛年份": 1997, "当选领导人年份": 2008, "进入政坛年龄": 36, "当选领导人年龄": 47, "多久当选领导人": 11, "政治路线": "中间"},
    {"国家": "波兰", "姓名": "唐纳德·图斯克", "出生年份": 1957, "学历": "历史", "任期年数": 7.0, "进入政坛年份": 1991, "当选领导人年份": 2007, "进入政坛年龄": 34, "当选领导人年龄": 50, "多久当选领导人": 16, "政治路线": "右翼"},
    {"国家": "俄罗斯", "姓名": "弗拉基米尔·普京", "出生年份": 1952, "学历": "法律", "任期年数": 24.0, "进入政坛年份": 1991, "当选领导人年份": 2012, "进入政坛年龄": 39, "当选领导人年龄": 60, "多久当选领导人": 21, "政治路线": "右翼"},
    {"国家": "西班牙", "姓名": "马里亚诺·拉霍伊", "出生年份": 1955, "学历": "法律", "任期年数": 7.0, "进入政坛年份": 1981, "当选领导人年份": 2011, "进入政坛年龄": 26, "当选领导人年龄": 56, "多久当选领导人": 30, "政治路线": "右翼"},
    {"国家": "瑞典", "姓名": "弗雷德里克·赖因费尔特", "出生年份": 1965, "学历": "理科/商业", "任期年数": 8.0, "进入政坛年份": 1991, "当选领导人年份": 2006, "进入政坛年龄": 26, "当选领导人年龄": 41, "多久当选领导人": 15, "政治路线": "右翼"},
    {"国家": "土耳其", "姓名": "雷杰普·塔伊普·埃尔多安", "出生年份": 1954, "学历": "商业", "任期年数": 11.0, "进入政坛年份": 1991, "当选领导人年份": 2003, "进入政坛年龄": 37, "当选领导人年龄": 49, "多久当选领导人": 12, "政治路线": "右翼"},
    {"国家": "英国", "姓名": "戴维·卡梅伦", "出生年份": 1966, "学历": "艺术/理科", "任期年数": 6.0, "进入政坛年份": 1997, "当选领导人年份": 2010, "进入政坛年龄": 31, "当选领导人年龄": 44, "多久当选领导人": 13, "政治路线": "右翼"},
    {"国家": "美国", "姓名": "贝拉克·奥巴马", "出生年份": 1961, "学历": "法律/理科", "任期年数": 8.0, "进入政坛年份": 1996, "当选领导人年份": 2009, "进入政坛年龄": 35, "当选领导人年龄": 48, "多久当选领导人": 13, "政治路线": "左翼"},
]

df = pd.DataFrame(raw_data)


# =========================
# 2) 数据映射规则
# =========================
def map_education_category(edu: str) -> str:
    """
    法律（含法律/理科） > 商业（含商业/理科） > 理科（含纯理科、艺术/理科） > 其他
    """
    edu = str(edu)
    if "法律" in edu:
        return "法律"
    elif "商业" in edu:
        return "商业"
    elif "理科" in edu:
        return "理科"
    else:
        return "其他"


def map_color(edu_cat: str) -> str:
    color_map = {
        "法律": "#1E40AF",  # 深蓝
        "理科": "#DC2626",  # 红色
        "商业": "#059669",  # 绿色
        "其他": "#64748B",  # 灰色
    }
    return color_map.get(edu_cat, "#64748B")


def map_symbol(route: str) -> str:
    symbol_map = {
        "右翼": "circle",
        "左翼": "square",
        "中间": "triangle-up",
    }
    return symbol_map.get(route, "circle")


def scale_size(years, min_years=2, max_years=24, min_px=10, max_px=60):
    years = max(min_years, min(max_years, years))
    return min_px + (years - min_years) * (max_px - min_px) / (max_years - min_years)


df["学历类别"] = df["学历"].apply(map_education_category)
df["颜色"] = df["学历类别"].apply(map_color)
df["形状"] = df["政治路线"].apply(map_symbol)
df["点大小"] = df["任期年数"].apply(scale_size)

df["hover_text"] = df.apply(
    lambda r: f"{r['国家']}-{r['姓名']}：{r['学历类别']}背景/{r['政治路线']}路线，执政{r['任期年数']}年",
    axis=1
)


# =========================
# 3) 交互参数
# =========================
# 区域分界线
X1, X2 = 30, 40
Y1, Y2 = 45, 55

QUAD_X = 30   # 22-30 视为“早进政坛”
QUAD_Y = 45   # 35-45 视为“早当选”

# 轴范围
X_RANGE = [20, 65]
Y_RANGE = [30, 75]   # 为了兼容 31 和 74


# =========================
# 4) 图形函数
# =========================
def build_trend_figure(current_year: int):
    year_counts = (
        df.groupby("进入政坛年份")
        .size()
        .reset_index(name="人数")
        .sort_values("进入政坛年份")
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=year_counts["进入政坛年份"],
            y=year_counts["人数"],
            name="年度进入政坛人数",
            marker_color="#94A3B8",
            hovertemplate="年份：%{x}<br>人数：%{y}<extra></extra>"
        )
    )

    fig.add_vline(
        x=current_year,
        line_width=3,
        line_dash="dash",
        line_color="#2563EB"
    )

    fig.update_layout(
        title="年度进入政坛人数趋势",
        height=240,
        margin=dict(l=40, r=20, t=50, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_xaxes(title="进入政坛年份", range=[1974.5, 2015.5], dtick=5, showgrid=False)
    fig.update_yaxes(title="人数", rangemode="tozero", gridcolor="#E5E7EB")
    return fig


def add_quadrant_shapes(fig, active_quadrant=None):
    quadrants = {
        "Q1": {"x0": 20, "x1": QUAD_X, "y0": QUAD_Y, "y1": 75, "label": "资深稳健型\n(早进政坛+晚当选)"},
        "Q2": {"x0": QUAD_X, "x1": 65, "y0": QUAD_Y, "y1": 75, "label": "长期积累型\n(晚进政坛+晚当选)"},
        "Q3": {"x0": 20, "x1": QUAD_X, "y0": 30, "y1": QUAD_Y, "label": "跨越式发展型\n(早进政坛+早当选)"},
        "Q4": {"x0": QUAD_X, "x1": 65, "y0": 30, "y1": QUAD_Y, "label": "政治新星型\n(晚进政坛+早当选)"},
    }

    for key, q in quadrants.items():
        fillcolor = "rgba(37,99,235,0.10)" if key == active_quadrant else "rgba(148,163,184,0.05)"
        linecolor = "rgba(37,99,235,0.35)" if key == active_quadrant else "rgba(148,163,184,0.20)"

        fig.add_shape(
            type="rect",
            x0=q["x0"], x1=q["x1"], y0=q["y0"], y1=q["y1"],
            line=dict(color=linecolor, width=1),
            fillcolor=fillcolor,
            layer="below"
        )

        fig.add_annotation(
            x=(q["x0"] + q["x1"]) / 2,
            y=(q["y0"] + q["y1"]) / 2,
            text=q["label"],
            showarrow=False,
            font=dict(size=11, color="#475569"),
            align="center"
        )

    # 分界线
    fig.add_vline(x=QUAD_X, line_dash="dash", line_color="#94A3B8", line_width=1.5)
    fig.add_hline(y=QUAD_Y, line_dash="dash", line_color="#94A3B8", line_width=1.5)


def build_scatter_figure(current_year: int, active_quadrant=None):
    filtered = df[df["进入政坛年份"] <= current_year].copy()

    # 若点选了四象限，则做高亮逻辑
    def in_quadrant(row, q):
        if q == "Q1":
            return row["进入政坛年龄"] <= QUAD_X and row["当选领导人年龄"] >= QUAD_Y
        elif q == "Q2":
            return row["进入政坛年龄"] > QUAD_X and row["当选领导人年龄"] >= QUAD_Y
        elif q == "Q3":
            return row["进入政坛年龄"] <= QUAD_X and row["当选领导人年龄"] < QUAD_Y
        elif q == "Q4":
            return row["进入政坛年龄"] > QUAD_X and row["当选领导人年龄"] < QUAD_Y
        return True

    if active_quadrant:
        filtered["高亮"] = filtered.apply(lambda r: in_quadrant(r, active_quadrant), axis=1)
    else:
        filtered["高亮"] = True

    fig = go.Figure()

    # 为了让“点击象限”可用，放四个透明可点击区域
    quadrant_polygons = {
        "Q1": ([22, QUAD_X, QUAD_X, 22, 22], [QUAD_Y, QUAD_Y, 75, 75, QUAD_Y], "资深稳健型"),
        "Q2": ([QUAD_X, 60, 60, QUAD_X, QUAD_X], [QUAD_Y, QUAD_Y, 75, 75, QUAD_Y], "长期积累型"),
        "Q3": ([22, QUAD_X, QUAD_X, 22, 22], [30, 30, QUAD_Y, QUAD_Y, 30], "跨越式发展型"),
        "Q4": ([QUAD_X, 60, 60, QUAD_X, QUAD_X], [30, 30, QUAD_Y, QUAD_Y, 30], "政治新星型"),
    }

    for qkey, (xs, ys, label) in quadrant_polygons.items():
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                fill="toself",
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
                hoverinfo="skip",
                customdata=[[f"quadrant:{qkey}"]] * len(xs),
                name=label,
                showlegend=False
            )
        )

    # 正常散点
    for route in ["右翼", "左翼", "中间"]:
        sub = filtered[filtered["政治路线"] == route]
        if sub.empty:
            continue

        opacity_values = [1.0 if x else 0.18 for x in sub["高亮"]]

        fig.add_trace(
            go.Scatter(
                x=sub["进入政坛年龄"],
                y=sub["当选领导人年龄"],
                mode="markers+text",
                text=sub["姓名"],
                textposition="top center",
                textfont=dict(size=11),
                customdata=sub[["国家", "姓名", "学历类别", "政治路线", "任期年数", "进入政坛年份"]].values,
                hovertemplate=(
                    "<b>%{customdata[0]} - %{customdata[1]}</b><br>"
                    "学历背景：%{customdata[2]}<br>"
                    "政治路线：%{customdata[3]}<br>"
                    "任期总时长：%{customdata[4]} 年<br>"
                    "进入政坛年份：%{customdata[5]}<br>"
                    "进入政坛年龄：%{x} 岁<br>"
                    "当选领导人年龄：%{y} 岁"
                    "<extra></extra>"
                ),
                marker=dict(
                    size=sub["点大小"],
                    color=sub["颜色"],
                    symbol=sub["形状"],
                    line=dict(color="white", width=1.2),
                    opacity=opacity_values
                ),
                name=route
            )
        )

    add_quadrant_shapes(fig, active_quadrant=active_quadrant)

    fig.update_layout(
        title=f"领导人政治晋升路径散点图（显示 {current_year} 年及以前进入政坛者）",
        dragmode="select",
        height=720,
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="政治路线（形状）",
    )

    fig.update_xaxes(
        title="进入政坛年龄",
        range=X_RANGE,
        tickmode="array",
        tickvals=[22, 25, 30, 35, 40, 45, 50, 55, 60],
        gridcolor="#E5E7EB"
    )

    fig.update_yaxes(
        title="当选领导人年龄",
        range=Y_RANGE,
        tickmode="array",
        tickvals=[30, 35, 45, 55, 65, 75],
        gridcolor="#E5E7EB"
    )

    # 区域注释
    fig.add_annotation(x=26, y=31.5, text="早慧型", showarrow=False, font=dict(color="#2563EB", size=12))
    fig.add_annotation(x=35, y=31.5, text="常规型", showarrow=False, font=dict(color="#2563EB", size=12))

    fig.add_annotation(x=22.8, y=40, text="快速晋升型", showarrow=False, textangle=-90, font=dict(color="#059669", size=12))
    fig.add_annotation(x=22.8, y=50, text="稳步发展型", showarrow=False, textangle=-90, font=dict(color="#059669", size=12))

    return fig


def format_stats(selected_points_df: pd.DataFrame) -> html.Div:
    if selected_points_df.empty:
        return html.Div([
            html.H4("框选统计"),
            html.P("请在散点图中拖拽框选或套索选择点。"),
            html.P("也可以点击某个四象限按钮，查看该区域高亮效果。")
        ])

    total = len(selected_points_df)
    route_counts = selected_points_df["政治路线"].value_counts().to_dict()
    edu_counts = selected_points_df["学历类别"].value_counts().to_dict()

    route_text = "；".join([f"{k}{v}人" for k, v in route_counts.items()]) if route_counts else "无"
    edu_text = "；".join([f"{k}背景{v}人" for k, v in edu_counts.items()]) if edu_counts else "无"

    reps = (
        selected_points_df.sort_values(["任期年数", "多久当选领导人"], ascending=[False, True])
        .head(3)[["姓名", "国家"]]
        .apply(lambda r: f"{r['姓名']}（{r['国家']}）", axis=1)
        .tolist()
    )
    rep_text = "、".join(reps)

    avg_enter_age = round(selected_points_df["进入政坛年龄"].mean(), 1)
    avg_leader_age = round(selected_points_df["当选领导人年龄"].mean(), 1)
    avg_tenure = round(selected_points_df["任期年数"].mean(), 1)

    return html.Div([
        html.H4("框选统计"),
        html.P(f"框选区域共 {total} 位领导人"),
        html.P(f"特征分布：{route_text}；{edu_text}"),
        html.P(f"代表人物：{rep_text}"),
        html.P(f"平均进入政坛年龄：{avg_enter_age} 岁"),
        html.P(f"平均当选领导人年龄：{avg_leader_age} 岁"),
        html.P(f"平均执政时长：{avg_tenure} 年"),
    ])


# =========================
# 5) Dash App
# =========================
app = Dash(__name__)
app.title = "领导人政治晋升可视化"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px", "background": "#F8FAFC"},
    children=[
        html.H2("领导人政治晋升路径可视化"),
        html.P("X轴：进入政坛年龄；Y轴：当选领导人年龄；点大小：任期总时长；点颜色：学历背景；点形状：政治路线。"),

        dcc.Store(id="play-state", data=False),
        dcc.Store(id="active-quadrant", data=None),

        html.Div([
            dcc.Graph(id="trend-chart"),
        ], style={"background": "white", "padding": "10px", "borderRadius": "12px", "marginBottom": "16px"}),

        html.Div([
            html.Button("播放", id="btn-play", n_clicks=0, style={"marginRight": "8px"}),
            html.Button("暂停", id="btn-pause", n_clicks=0, style={"marginRight": "8px"}),
            html.Button("重置", id="btn-reset", n_clicks=0, style={"marginRight": "20px"}),

            html.Span("播放速度：", style={"marginRight": "8px"}),
            dcc.RadioItems(
                id="speed-radio",
                options=[
                    {"label": "慢", "value": 1200},
                    {"label": "中", "value": 700},
                    {"label": "快", "value": 350},
                ],
                value=700,
                inline=True
            ),
        ], style={"marginBottom": "10px"}),

        dcc.Slider(
            id="year-slider",
            min=1975,
            max=2015,
            step=1,
            value=2015,
            marks={year: str(year) for year in range(1975, 2016, 5)},
            tooltip={"placement": "bottom", "always_visible": True},
        ),

        dcc.Interval(
            id="play-interval",
            interval=700,
            n_intervals=0,
            disabled=True
        ),

        html.Div([
            html.Div([
                html.Div("四象限筛选", style={"fontWeight": "bold", "marginBottom": "8px"}),

                html.Button("资深稳健型（左上）", id="q1-btn", n_clicks=0, style={"margin": "4px"}),
                html.Button("长期积累型（右上）", id="q2-btn", n_clicks=0, style={"margin": "4px"}),
                html.Button("跨越式发展型（左下）", id="q3-btn", n_clicks=0, style={"margin": "4px"}),
                html.Button("政治新星型（右下）", id="q4-btn", n_clicks=0, style={"margin": "4px"}),
                html.Button("清除高亮", id="clear-q-btn", n_clicks=0, style={"margin": "4px"}),
            ], style={
                "background": "white",
                "padding": "12px",
                "borderRadius": "12px",
                "marginBottom": "16px"
            }),
        ]),

        html.Div([
            html.Div([
                dcc.Graph(id="scatter-chart", clear_on_unhover=True),
            ], style={"width": "72%", "display": "inline-block", "verticalAlign": "top"}),

            html.Div([
                html.Div(
                    id="selection-stats",
                    style={
                        "background": "white",
                        "padding": "16px",
                        "borderRadius": "12px",
                        "minHeight": "240px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.08)"
                    }
                ),
                html.Div([
                    html.H4("图例说明"),
                    html.Ul([
                        html.Li("颜色：法律=深蓝；理科=红；商业=绿；其他=灰"),
                        html.Li("形状：右翼=圆形；左翼=方形；中间=三角形"),
                        html.Li("拖拽框选 / 套索可查看局部统计"),
                        html.Li("时间轴可回放不同年份进入政坛的人群")
                    ])
                ], style={
                    "background": "white",
                    "padding": "16px",
                    "borderRadius": "12px",
                    "marginTop": "16px",
                    "boxShadow": "0 1px 3px rgba(0,0,0,0.08)"
                })
            ], style={"width": "26%", "display": "inline-block", "marginLeft": "2%", "verticalAlign": "top"})
        ])
    ]
)


# =========================
# 6) 回调：播放状态
# =========================
@app.callback(
    Output("play-state", "data"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    State("play-state", "data"),
    prevent_initial_call=True
)
def control_play(play_clicks, pause_clicks, reset_clicks, current_state):
    trigger = callback_context.triggered_id
    if trigger == "btn-play":
        return True
    elif trigger == "btn-pause":
        return False
    elif trigger == "btn-reset":
        return False
    return current_state


@app.callback(
    Output("play-interval", "disabled"),
    Output("play-interval", "interval"),
    Input("play-state", "data"),
    Input("speed-radio", "value"),
)
def update_interval(play_state, speed_value):
    return (not play_state), speed_value


@app.callback(
    Output("year-slider", "value"),
    Input("play-interval", "n_intervals"),
    Input("btn-reset", "n_clicks"),
    State("year-slider", "value"),
    State("play-state", "data"),
    prevent_initial_call=True
)
def auto_advance_year(n_intervals, reset_clicks, current_year, play_state):
    trigger = callback_context.triggered_id
    if trigger == "btn-reset":
        return 1975
    if play_state:
        return 1975 if current_year >= 2015 else current_year + 1
    return current_year


# =========================
# 7) 回调：四象限按钮
# =========================
@app.callback(
    Output("active-quadrant", "data"),
    Input("q1-btn", "n_clicks"),
    Input("q2-btn", "n_clicks"),
    Input("q3-btn", "n_clicks"),
    Input("q4-btn", "n_clicks"),
    Input("clear-q-btn", "n_clicks"),
    State("active-quadrant", "data"),
    prevent_initial_call=True
)
def update_quadrant(q1, q2, q3, q4, clear_q, current_q):
    trigger = callback_context.triggered_id
    if trigger == "q1-btn":
        return "Q1"
    elif trigger == "q2-btn":
        return "Q2"
    elif trigger == "q3-btn":
        return "Q3"
    elif trigger == "q4-btn":
        return "Q4"
    elif trigger == "clear-q-btn":
        return None
    return current_q


# =========================
# 8) 回调：图形更新
# =========================
@app.callback(
    Output("scatter-chart", "figure"),
    Output("trend-chart", "figure"),
    Input("year-slider", "value"),
    Input("active-quadrant", "data")
)
def update_figures(year_value, active_quadrant):
    scatter_fig = build_scatter_figure(year_value, active_quadrant)
    trend_fig = build_trend_figure(year_value)
    return scatter_fig, trend_fig


# =========================
# 9) 回调：框选统计
# =========================
@app.callback(
    Output("selection-stats", "children"),
    Input("scatter-chart", "selectedData"),
    Input("year-slider", "value")
)
def update_selection_stats(selected_data, year_value):
    current_df = df[df["进入政坛年份"] <= year_value].copy()

    if not selected_data or "points" not in selected_data:
        return format_stats(pd.DataFrame())

    selected_names = []
    for p in selected_data["points"]:
        custom = p.get("customdata", None)
        # customdata 对领导人点是 [国家, 姓名, 学历类别, 政治路线, 任期年数, 进入政坛年份]
        if isinstance(custom, list) and len(custom) >= 2 and not str(custom[0]).startswith("quadrant:"):
            selected_names.append(custom[1])

    selected_df = current_df[current_df["姓名"].isin(selected_names)].copy()
    return format_stats(selected_df)


if __name__ == "__main__":
    app.run(debug=True)