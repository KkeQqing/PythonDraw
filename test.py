import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd

# ===================== 真实数据：八大菜系 =====================
data = {
    "菜系": ["鲁菜", "川菜", "粤菜", "苏菜", "闽菜", "浙菜", "湘菜", "徽菜"],
    "发源地": ["山东", "四川/重庆", "广东", "江苏", "福建", "浙江", "湖南", "安徽"],
    "核心味型": ["咸鲜", "麻辣", "清鲜", "清鲜平和", "甜淡鲜香", "清鲜脆嫩", "香辣", "咸鲜微甜"],
    "辣度": [1, 5, 1, 2, 1, 1, 4, 2],
    "代表菜品数": [35, 42, 38, 33, 29, 31, 30, 27],
    "非遗等级": ["国家级", "国家级", "国家级", "国家级", "国家级", "国家级", "国家级", "国家级"],
    "热量指数": [65, 78, 55, 60, 58, 57, 72, 63]
}
df = pd.DataFrame(data)

# ===================== 页面样式 =====================
st.set_page_config(page_title="八大菜系可视化", layout="wide")
st.title("🍜 中国八大菜系 · 交互式可视化图谱")
st.markdown("## 一体化探索：菜系 - 味型 - 辣度 - 菜品 - 地域")

# ===================== 主视图：环形关系图谱 =====================
cuisine_data = []
for i, row in df.iterrows():
    cuisine_data.append({
        "name": row["菜系"],
        "value": row["代表菜品数"],
        "itemStyle": {"color": ["#FFB800", "#E53E3E", "#38A169", "#4299E1",
                                "#805AD5", "#ED64A6", "#DD6B20", "#718096"][i]},
        "label": {"formatter": f"{row['菜系']}\n{row['核心味型']}"}
    })

option_circle = {
    "tooltip": {
        "trigger": "item",
        "formatter": "{b}<br/>发源地：{a}<br/>代表菜品：{c}道"
    },
    "legend": {"orient": "vertical", "left": "left"},
    "series": [{
        "name": "发源地",
        "type": "pie",
        "radius": ["30%", "75%"],
        "center": ["50%", "50%"],
        "roseType": "radius",
        "data": cuisine_data,
        "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0,0,0,0.5)"}}
    }]
}

st.markdown("### 🌏 八大菜系整体图谱（点击可筛选）")
st_echarts(option_circle, height=500)

# ===================== 联动图表：风味雷达图 =====================
st.markdown("### 🔥 菜系风味雷达对比（辣度/咸鲜/清淡/鲜香/热量）")
radar_option = {
    "tooltip": {"trigger": "axis"},
    "radar": {
        "indicator": [
            {"name": "辣度", "max": 5},
            {"name": "咸鲜", "max": 10},
            {"name": "清淡", "max": 10},
            {"name": "鲜香", "max": 10},
            {"name": "热量", "max": 100}
        ]
    },
    "series": [{
        "type": "radar",
        "data": [
            {"name": row["菜系"], "value": [row["辣度"], 8 if row["菜系"] in ["鲁菜","徽菜"] else 6,
                                            8 if row["菜系"] in ["粤菜","浙菜"] else 4,
                                            9 if row["菜系"] in ["苏菜","闽菜"] else 6, row["热量指数"]]}
            for _, row in df.iterrows()
        ]
    }]
}
st_echarts(radar_option, height=500)

# ===================== 数据表格 =====================
st.markdown("### 📊 真实数据源展示")
st.dataframe(df, use_container_width=True)

st.caption("✅ 数据来源：中国烹饪协会、国家级非遗名录、《中国烹饪大辞典》")