import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from ipywidgets import widgets, interact, FloatSlider, Button, HBox, VBox, Output
import threading
import time

# ===================== 全局设置 =====================
pio.renderers.default = "browser"  # 自动在浏览器打开

# ===================== 1. 精准数据 =====================
data = [
    {"物体": "拳套", "最高速度": 56, "反应时间": 0.064, "对应距离": 1},
    {"物体": "乒乓球", "最高速度": 88, "反应时间": 0.112, "对应距离": 2.74},
    {"物体": "足球（点球）", "最高速度": 112, "反应时间": 0.35, "对应距离": 10.9},
    {"物体": "羽毛球", "最高速度": 160, "反应_time": 0.225, "对应距离": 10},
    {"物体": "棒球", "最高速度": 160, "反应时间": 0.4149, "对应距离": 18.4},
    {"物体": "网球", "最高速度": 160, "反应时间": 0.534, "对应距离": 24},
    {"物体": "法拉利 458", "最高速度": 320, "反应时间": 0.64, "对应距离": 402},
]
df = pd.DataFrame(data)
df = df.sort_values("反应时间").reset_index(drop=True)

# ===================== 2. 统一配色（严格按设计） =====================
color_map = {
    "拳套": "#78909C",
    "乒乓球": "#42A5F5",
    "足球（点球）": "#66BB6A",
    "羽毛球": "#FFD700",  # 亮黄色
    "棒球": "#FFA726",
    "网球": "#AB47BC",
    "法拉利 458": "#E53935"  # 红色
}


# ===================== 工具函数 =====================
def calculate_reaction_time(distance, speed_kmh):
    speed_ms = speed_kmh * 1000 / 3600
    return round(distance / speed_ms, 3)


# ===================== 模块1：主条形图（维度切换 + 悬停 + 多选） =====================
def create_main_bar():
    fig = px.bar(
        df,
        x="物体",
        y="反应时间",
        color="物体",
        color_discrete_map=color_map,
        text="反应时间",
        title="物体反应速度对比（默认：反应时间）",
        labels={"反应时间": "反应时间（秒）", "物体": ""}
    )

    # 顶部数值标注
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        textfont=dict(size=13),
        hovertemplate=""
    )

    # 悬停卡片（含公式）
    hover_text = []
    for i, row in df.iterrows():
        speed = row["最高速度"]
        dist = row["对应距离"]
        time_val = row["反应时间"]
        speed_ms = round(speed / 3.6, 2)
        txt = f"<b>{row['物体']}</b><br>"
        txt += f"速度：{speed} km/h<br>"
        txt += f"距离：{dist} m<br>"
        txt += f"反应时间：{time_val} s<br><br>"
        txt += f"公式：{dist}m ÷ ({speed}km/h = {speed_ms}m/s) ≈ {time_val}s"
        hover_text.append(txt)

    fig.update_traces(customdata=hover_text, hovertemplate="%{customdata}")

    # 维度切换按钮 + 自动排序
    fig.update_layout(
        showlegend=False,
        height=550,
        margin=dict(t=80, b=40),
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.05, y=1.15,
            buttons=[
                dict(
                    label="反应时间（秒）",
                    method="update",
                    args=[
                        {"y": [df.sort_values("反应时间")["反应时间"]],
                         "x": [df.sort_values("反应时间")["物体"]]},
                        {"yaxis.title.text": "反应时间（秒）",
                         "title.text": "反应时间对比（从短到长）"}
                    ]
                ),
                dict(
                    label="最高速度（km/h）",
                    method="update",
                    args=[
                        {"y": [df.sort_values("最高速度", ascending=False)["最高速度"]],
                         "x": [df.sort_values("最高速度", ascending=False)["物体"]]},
                        {"yaxis.title.text": "最高速度（km/h）",
                         "title.text": "最高速度对比（从高到低）"}
                    ]
                ),
                dict(
                    label="对应距离（米）",
                    method="update",
                    args=[
                        {"y": [df.sort_values("对应距离")["对应距离"]],
                         "x": [df.sort_values("对应距离")["物体"]]},
                        {"yaxis.title.text": "对应距离（米）",
                         "title.text": "对应距离对比（从短到长）"}
                    ]
                )
            ]
        )]
    )
    return fig


# ===================== 模块2：反应时间计算器（动态） =====================
def create_time_calculator():
    @interact(distance=FloatSlider(min=1, max=500, value=10, description="距离(m)"))
    def update(distance=10):
        temp = df.copy()
        temp["计算时间"] = temp["最高速度"].apply(lambda s: calculate_reaction_time(distance, s))
        temp = temp.sort_values("计算时间")

        fig = px.bar(
            temp, x="物体", y="计算时间", color="物体",
            color_discrete_map=color_map, text="计算时间",
            title=f"自定义距离：{distance} 米 · 实时反应时间"
        )
        fig.update_traces(textposition='outside', textfont_size=13)
        fig.update_layout(height=500, showlegend=False)
        fig.show()


# ===================== 模块3：模拟飞行动画 =====================
def run_animation(distance=10):
    temp = df.copy()
    temp["时间"] = temp["最高速度"].apply(lambda s: calculate_reaction_time(distance, s))
    max_t = temp["时间"].max()

    print(f"\n🎬 开始模拟：距离 = {distance} 米")
    print(f"⏱ 总时长：{max_t:.2f} 秒")
    print("-" * 50)

    start_time = time.time()
    finished = {}

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_t + 0.5:
            break

        print(f"\r⏳ 已用时：{elapsed:.2f}s / {max_t:.2f}s", end="")

        for _, row in temp.iterrows():
            name = row["物体"]
            t_total = row["时间"]
            if name in finished:
                continue

            progress = min(elapsed / t_total, 1.0) if t_total > 0 else 1.0
            pos = int(progress * 50)

            if progress >= 1:
                finished[name] = t_total
                print(f"\n✅ {name} 到达终点 | 时间：{t_total:.3f}s")

        time.sleep(0.05)

    print("\n" + "-" * 50)
    bad = finished.get("法拉利 458", 0)
    ym = finished.get("羽毛球", 0)
    if ym > 0 and bad > 0:
        delta = bad - ym
        print(f"🔍 结论：{distance}米下，羽毛球({ym:.3f}s) 比 法拉利({bad:.3f}s) 快 {delta:.3f}s")


# ===================== 模块4：三维雷达图（归一化） =====================
def create_radar():
    df_norm = df.copy()
    df_norm["速度_100"] = df_norm["最高速度"] / df_norm["最高速度"].max() * 100
    df_norm["时间_100"] = (1 / df_norm["反应时间"]) / (1 / df_norm["反应时间"]).min() * 100
    df_norm["距离_100"] = df_norm["对应距离"] / df_norm["对应距离"].max() * 100

    fig = go.Figure()
    for _, row in df_norm.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["速度_100"], row["时间_100"], row["距离_100"]],
            theta=["最高速度", "反应速度", "对应距离"],
            fill="toself",
            name=row["物体"],
            opacity=0.3,
            marker=dict(color=color_map[row["物体"]]),
            hovertemplate=f"<b>{row['物体']}</b><br>速度：%{{r:.0f}}%<br>反应速度：%{{r:.0f}}%<br>距离：%{{r:.0f}}%"
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        title="三维综合能力雷达图",
        height=550
    )
    return fig


# ===================== 启动所有功能 =====================
if __name__ == "__main__":
    print("=" * 60)
    print(" 交互式可视化：速度 / 反应时间 / 距离")
    print("=" * 60)

    # 1. 主条形图（维度切换）
    print("\n[1] 正在打开：主条形图（维度切换 + 悬停公式）...")
    main_fig = create_main_bar()
    main_fig.show()

    # 2. 雷达图
    print("\n[2] 正在打开：三维雷达图...")
    radar_fig = create_radar()
    radar_fig.show()

    # 3. 时间计算器
    print("\n[3] 启动：反应时间计算器（拖动滑块）...")
    create_time_calculator()

    # 4. 飞行动画
    print("\n[4] 启动：模拟飞行动画（默认10米）...")
    run_animation(10)

    print("\n🎉 全部功能已启动！")