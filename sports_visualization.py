import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


# 启动：streamlit run sports_visualization.py

# -------------------------- 1. 数据配置 --------------------------
data = {
    "物体": ["拳套", "乒乓球", "足球", "羽毛球", "棒球", "网球", "法拉利 458"],
    "最高速度（千米/时）": [56, 88, 112, 160, 160, 160, 320],
    "反应时间（秒）": [0.064, 0.112, 0.35, 0.225, 0.4149, 0.534, 0.64],
    "对应距离（米）": [1, 2.74, 10.9, 10, 18.4, 24, 402]
}
df = pd.DataFrame(data)

color_map = {
    "羽毛球": "#FFD700",  # 亮黄色
    "法拉利 458": "#FF0000",  # 红色
    "拳套": "#8B4513",  # 棕色
    "乒乓球": "#1E90FF",  # 蓝色
    "足球": "#32CD32",  # 绿色
    "棒球": "#FF6347",  # 红色
    "网球": "#FFA500"  # 橙色
}

# -------------------------- 页面基础设置 --------------------------
st.set_page_config(
    page_title="物体运动数据可视化",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("物体运动数据可视化")
st.markdown("---")

# -------------------------- 侧边栏控制面板 --------------------------
with st.sidebar:
    st.header("控制面板")

    # 视图切换
    view_mode = st.radio(
        "选择视图模式",
        ["动态条形图", "三维雷达图", "飞行模拟动画"]
    )

    st.markdown("### 数据维度")
    y_axis_option = st.radio(
        "切换Y轴维度",
        ["反应时间（秒）", "最高速度（千米/时）", "对应距离（米）"]
    )

    st.markdown("### 物体多选对比")
    all_items = df["物体"].tolist()
    selected_items = st.multiselect(
        "勾选对比对象",
        options=all_items,
        default=all_items
    )

    # 计算器：自定义距离
    st.markdown("### 反应时间计算器")
    custom_distance = st.number_input(
        "自定义对比距离（米）",
        min_value=1.0, max_value=500.0, value=50.0, step=0.1
    )

    # 动画速度
    if view_mode == "飞行模拟动画":
        st.markdown("### 动画设置")
        anim_speed = st.select_slider("播放速度", options=[0.5, 1, 2], value=1)

# 筛选数据
df_filtered = df[df["物体"].isin(selected_items)].copy()


# -------------------------- 工具函数 --------------------------
def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6


def calc_reaction_time(distance, speed_kmh):
    ms = kmh_to_ms(speed_kmh)
    return distance / ms if ms != 0 else 0


# -------------------------- 视图1：动态条形图 --------------------------
if view_mode == "动态条形图":
    st.subheader("动态条形图（维度切换 + 对比分析）")

    # 排序逻辑
    if y_axis_option == "最高速度（千米/时）":
        df_sorted = df_filtered.sort_values(by=y_axis_option, ascending=False)
    elif y_axis_option == "对应距离（米）":
        df_sorted = df_filtered.sort_values(by=y_axis_option, ascending=True)
    else:
        df_sorted = df_filtered.sort_values(by=y_axis_option, ascending=True)

    # 绘图
    fig = px.bar(
        df_sorted,
        x="物体",
        y=y_axis_option,
        color="物体",
        color_discrete_map=color_map,
        text_auto=".2f",
        title=f"按【{y_axis_option}】排序对比",
        height=550
    )

    # 样式优化
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=14, color="black"),
        marker_line_width=2,
        marker_line_color="white",
        hovertemplate="<b>%{x}</b><br>"
                      f"{y_axis_option}: %{{y:.2f}}<br>"
                      "最高速度: %{customdata[0]:.0f} km/h<br>"
                      "反应时间: %{customdata[1]:.3f} s<br>"
                      "对应距离: %{customdata[2]:.1f} m",
        customdata=df_sorted[["最高速度（千米/时）", "反应时间（秒）", "对应距离（米）"]].values
    )

    fig.update_layout(
        yaxis_title=y_axis_option,
        xaxis_title="物体",
        showlegend=False,
        transition_duration=300,
        plot_bgcolor="white",
        paper_bgcolor="white",

        # 轴标题字体
        xaxis=dict(
            title_font=dict(size=15, color="black", family="Arial Bold"),

            tickfont=dict(size=14, color="black")
        ),
        yaxis=dict(
            title_font=dict(size=15, color="black", family="Arial Bold"),
            tickfont=dict(size=14, color="black")
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# -------------------------- 视图2：三维雷达图 --------------------------
elif view_mode == "三维雷达图":
    st.subheader("三维雷达图（速度 / 反应时间 / 对应距离 综合对比）")

    # 归一化 0~100%
    df_radar = df_filtered.copy()
    df_radar["速度归一化"] = df_radar["最高速度（千米/时）"] / df["最高速度（千米/时）"].max() * 100
    df_radar["反应时间归一化"] = (df_radar["反应时间（秒）"] / df["反应时间（秒）"].max()) * 100
    df_radar["对应距离归一化"] = df_radar["对应距离（米）"] / df["对应距离（米）"].max() * 100

    fig = go.Figure()
    categories = ["最高速度", "反应时间", "对应距离"]  # 明确标注三个维度

    for _, row in df_radar.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["速度归一化"], row["反应时间归一化"], row["对应距离归一化"]],
            theta=categories,
            fill="toself",
            name=row["物体"],
            marker=dict(color=color_map[row["物体"]]),
            opacity=0.3,
            hovertemplate=f"<b>{row['物体']}</b><br>"
                          f"最高速度: {row['速度归一化']:.0f}%<br>"
                          f"反应时间: {row['反应时间归一化']:.0f}%<br>"
                          f"对应距离: {row['对应距离归一化']:.0f}%"
        ))

    fig.update_layout(
        polar=dict(

            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=13, color="black"),
                tickcolor="black",
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0%", "20%", "40%", "60%", "80%", "100%"]
            ),
            angularaxis=dict(
                tickfont=dict(size=15, color="white", family="Arial Bold"),
                tickcolor="white"
            )
        ),
        height=600,
        title="三维综合能力雷达图（100% = 该项最大值）<br>维度：最高速度 | 反应时间 | 对应距离",
        font=dict(color="black", size=14)
    )
    st.plotly_chart(fig, use_container_width=True)


# -------------------------- 视图3：飞行模拟动画 --------------------------
elif view_mode == "飞行模拟动画":
    st.subheader("统一距离飞行模拟（实时动画）")
    st.info(f"当前统一距离：**{custom_distance} 米** | 动画速度：{anim_speed}x")

    # 计算到达时间
    df_anim = df_filtered.copy()
    df_anim["到达时间（秒）"] = df_anim["最高速度（千米/时）"].apply(
        lambda x: calc_reaction_time(custom_distance, x)
    )
    df_anim = df_anim.sort_values("到达时间（秒）")

    # 动画控制

    col_anim1, col_anim2 = st.columns(2)
    start = col_anim1.button("开始模拟")
    reset = col_anim2.button("重置")

    # 赛道画布
    fig_track = go.Figure()
    fig_track.update_layout(
        xaxis=dict(range=[0, custom_distance * 1.1], title="距离（米）"),
        yaxis=dict(range=[-1, len(selected_items)], title="物体", tickmode="array",
                   tickvals=list(range(len(selected_items))), ticktext=df_anim["物体"].tolist()),
        height=500,
        title="赛道实时位置"
    )

    # 绘制起点/终点
    fig_track.add_vline(x=0, line_width=3, line_color="green", annotation_text="起点")
    fig_track.add_vline(x=custom_distance, line_width=3, line_color="red", annotation_text="终点")

    # 绘制物体初始位置
    for i, (_, row) in enumerate(df_anim.iterrows()):
        fig_track.add_trace(go.Scatter(
            x=[0], y=[i], mode="markers+text",
            marker=dict(color=color_map[row["物体"]], size=12),
            text=row["物体"], textposition="top center",
            name=row["物体"]
        ))

    chart = st.plotly_chart(fig_track, use_container_width=True)
    time_display = st.empty()

    if start:
        max_time = df_anim["到达时间（秒）"].max()
        t = 0.0
        step = 0.05 / anim_speed

        while t <= max_time:
            fig_track.data = []
            fig_track.add_vline(x=0, line_width=3, line_color="green")
            fig_track.add_vline(x=custom_distance, line_width=3, line_color="red")

            for i, (_, row) in enumerate(df_anim.iterrows()):
                arrive_t = row["到达时间（秒）"]
                if t >= arrive_t:
                    pos = custom_distance
                else:
                    pos = kmh_to_ms(row["最高速度（千米/时）"]) * t

                fig_track.add_trace(go.Scatter(
                    x=[pos], y=[i], mode="markers+text",
                    marker=dict(color=color_map[row["物体"]], size=14),
                    text=f"{row['物体']} ({pos:.1f}m)", textposition="top center"
                ))

            time_display.metric("已用时间", f"{t:.2f} s / {max_time:.2f} s")
            chart.plotly_chart(fig_track, use_container_width=True)
            t += step


        st.success(f"模拟完成！")
        badminton = df_anim[df_anim["物体"] == "羽毛球"]["到达时间（秒）"].values
        ferrari = df_anim[df_anim["物体"] == "法拉利 458"]["到达时间（秒）"].values

st.markdown("---")