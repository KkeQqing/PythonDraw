import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ==========================================
# 1. 数据准备
# ==========================================
# 模拟八大菜系数据
cuisines_data = [
    {"name": "川菜", "color": "#FF4500", "value": 95, "radar": [20, 30, 10, 90, 60, 80], "desc": "一菜一格，百菜百味。以善用三椒著称。"},
    {"name": "粤菜", "color": "#FFD700", "value": 98, "radar": [10, 40, 5, 10, 70, 95], "desc": "选料杂博，鲜嫩滑爽。讲究镬气和原汁原味。"},
    {"name": "鲁菜", "color": "#DAA520", "value": 85, "radar": [10, 20, 5, 10, 80, 90], "desc": "宫廷最大菜系，技法丰富。擅长爆、烧、炸、炒。"},
    {"name": "苏菜", "color": "#32CD32", "value": 80, "radar": [15, 60, 5, 5, 50, 85], "desc": "口味平和，鲜香酥嫩。擅长炖、焖、蒸、炒。"},
    {"name": "浙菜", "color": "#20B2AA", "value": 75, "radar": [15, 50, 5, 5, 40, 80], "desc": "制作精细，清鲜爽脆。具有江南水乡的秀丽风格。"},
    {"name": "闽菜", "color": "#FF69B4", "value": 70, "radar": [40, 30, 5, 15, 60, 95], "desc": "汤路广泛，鲜香多味。尤以'香'、'味'见长。"},
    {"name": "湘菜", "color": "#FF0000", "value": 88, "radar": [10, 20, 5, 85, 75, 70], "desc": "油重色浓，酸辣鲜香。注重香辣、香鲜、软嫩。"},
    {"name": "徽菜", "color": "#8B4513", "value": 65, "radar": [10, 30, 5, 20, 70, 75], "desc": "重油重色重火功。擅长烧、炖，讲究食补。"}
]

df = pd.DataFrame(cuisines_data)

# 计算每个菜系在半圆环上的角度 (-90度 到 90度)
# 我们让它们均匀分布在右侧半圆
df['angle'] = np.linspace(-90, 90, len(df))

# ==========================================
# 2. 初始化 Dash 应用
# ==========================================
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'display': 'flex',
        'height': '100vh',
        'background-color': '#111111',
        'font-family': 'Arial, sans-serif',
        'color': 'white',
        'overflow': 'hidden'
    },
    children=[
        # --- 左侧：数据展示区 ---
        html.Div(
            id='left-panel',
            style={
                'flex': '1',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '50px',
                'borderRight': '1px solid #333'
            },
            children=[
                html.H1("中华饮食基因图谱", style={'color': '#888'}),
                html.P("请在右侧半圆环中选择菜系", style={'color': '#555'})
            ]
        ),

        # --- 右侧：可视化交互区 ---
        html.Div(
            style={'flex': '1', 'position': 'relative'},
            children=[
                dcc.Graph(
                    id='cuisine-ring',
                    style={'height': '100%', 'width': '100%'},
                    config={'displayModeBar': False} # 隐藏工具栏
                )
            ]
        )
    ]
)

# ==========================================
# 3. 回调逻辑 (核心交互)
# ==========================================
@app.callback(
    [Output('cuisine-ring', 'figure'),
     Output('left-panel', 'children')],
    [Input('cuisine-ring', 'clickData')]
)
def update_dashboard(clickData):
    # 默认选中第一个，或者如果点击了某个点则选中那个
    selected_name = None
    if clickData:
        selected_name = clickData['points'][0]['customdata']

    if not selected_name:
        selected_name = df.iloc[0]['name']

    # 获取选中菜系的详细数据
    selected_row = df[df['name'] == selected_name].iloc[0]

    # --- 构建 Plotly 图表 ---
    fig = go.Figure()

    # A. 绘制背景轨道 (半圆环)
    fig.add_trace(go.Scatterpolar(
        r=[100] * 100,
        theta=np.linspace(-90, 90, 100),
        mode='lines',
        line=dict(color='#333', width=20),
        hoverinfo='skip',
        showlegend=False
    ))

    # B. 绘制菜系节点
    for i, row in df.iterrows():
        is_selected = row['name'] == selected_name

        # 连线逻辑：如果选中，画一条线指向左侧
        if is_selected:
            # 画连接线 (从圆环指向左侧面板中心)
            fig.add_trace(go.Scatterpolar(
                r=[100, 140], # 线条长度
                theta=[row['angle'], row['angle']],
                mode='lines+text',
                line=dict(color=row['color'], width=4, dash='dot'),
                text=[None, "👈 详情"],
                textposition="top right",
                hoverinfo='skip',
                showlegend=False
            ))

            # 高亮选中节点
            fig.add_trace(go.Scatterpolar(
                r=[100],
                theta=[row['angle']],
                mode='markers+text',
                marker=dict(size=30, color=row['color'], line=dict(width=4, color='white')),
                text=[row['name']],
                textposition="middle center",
                textfont=dict(color="white", size=12),
                customdata=[row['name']],
                hoverinfo='text',
                hovertext=f"<b>{row['name']}</b><br>影响力: {row['value']}",
                showlegend=False
            ))
        else:
            # 未选中节点 (显示为小点)
            fig.add_trace(go.Scatterpolar(
                r=[100],
                theta=[row['angle']],
                mode='markers+text',
                marker=dict(size=15, color='#555', line=dict(width=1, color='#333')),
                text=[row['name']],
                textposition="middle center",
                textfont=dict(color="white", size=10),
                customdata=[row['name']],
                hoverinfo='text',
                hovertext=row['name'],
                showlegend=False
            ))

    # C. 图表布局设置
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 150]),
            angularaxis=dict(visible=False, direction="clockwise", period=360)
        ),
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        clickmode='event+select'
    )

    # --- 构建左侧 HTML 内容 ---
    # 雷达图配置
    radar_categories = ['酸', '甜', '苦', '辣', '咸', '鲜']

    left_content = [
        html.H2(f"{selected_row['name']} · 深度解析", style={'borderBottom': f'2px solid {selected_row["color"]}', 'paddingBottom': '10px'}),
        html.P(selected_row['desc'], style={'fontSize': '18px', 'lineHeight': '1.6', 'color': '#ccc', 'maxWidth': '500px'}),

        html.Div(style={'display': 'flex', 'gap': '40px', 'marginTop': '30px', 'alignItems': 'center'}, children=[
            # 雷达图容器
            html.Div(style={'width': '400px'}, children=[
                dcc.Graph(
                    id='radar-chart',
                    figure=go.Figure(
                        data=go.Scatterpolar(
                            r=selected_row['radar'],
                            theta=radar_categories,
                            fill='toself',
                            line_color=selected_row['color'],
                            marker_color=selected_row['color']
                        )
                    ).update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#888')),
                            angularaxis=dict(tickfont=dict(color='white'))
                        ),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=20, r=20, t=20, b=20),
                        showlegend=False
                    ),
                    config={'displayModeBar': False}
                )
            ]),

            # 关键指标
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}, children=[
                html.Div([html.Span("风味主调:", style={'color': '#888'}), f" {radar_categories[np.argmax(selected_row['radar'])]}"]),
                html.Div([html.Span("影响力指数:", style={'color': '#888'}), f" {selected_row['value']}/100"]),
                html.Div([html.Span("代表技法:", style={'color': '#888'}), " 爆、炒、蒸"]),
                html.Div(style={'marginTop': '20px'}, children=[
                    html.Button("查看代表名菜", style={'backgroundColor': selected_row['color'], 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer', 'borderRadius': '5px'})
                ])
            ])
        ])
    ]

    return fig, left_content

# ==========================================
# 4. 启动服务器
# ==========================================
if __name__ == '__main__':
    # 新版本写法
    app.run(debug=True)