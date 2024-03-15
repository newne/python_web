import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def main():
    st.set_page_config(
        page_title="平面拟合",
        page_icon="",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={"About": "Wei Qian copyright",},
    )
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        st.write("filename:", uploaded_file.name)
        df = pd.read_csv(uploaded_file)
        df.columns = ["x", "y", "z"]
        st.dataframe(df, use_container_width=True)
        if df.empty:
            st.warning("No data found")
            return
        points = df.values

        # 计算点云的质心
        centroid = np.mean(points, axis=0)

        # 将点云的质心平移到原点
        points_centered = points - centroid

        # 使用SVD分解质心化后的点云矩阵
        U, S, Vt = np.linalg.svd(points_centered)

        # 平面的法向量是Vt矩阵的最后一列
        normal = Vt[-1, :]

        # 确保法向量指向z轴正方向
        if normal[2] < 0:
            normal = -normal

        # 平面方程：ax + by + cz = d
        # 其中(a, b, c)是法向量，d是原点到平面的距离
        a, b, c = normal

        d = -np.dot(normal, centroid)
        print("平面拟合结果为： %.3f * x + %.3f * y + %.3f*z + %3.f=0" % (a, b, c, d))
        fig = draw_plane(a, b, c, d, points)
        st.write("平面拟合结果为： %.3f * x + %.3f * y + %.3f*z + %3.f=0 " % (a, b, c, d))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        pred = pd.read_csv("data/predict.csv")
        pred.columns = ["x", "y"]
        pred["z"] = pred.apply(cal_z, args=(a, b, c, d,), axis=1)
        st.dataframe(pred, use_container_width=True)
        st.write("this is pred:")
        fig = draw_plane(a, b, c, d, pred.values)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_plane(a, b, c, d, points):
    # 创建平面网格
    x_range = np.linspace(np.min(points[:, 0]), np.max(points[:, 0]), 30)
    y_range = np.linspace(np.min(points[:, 1]), np.max(points[:, 1]), 30)
    x_grid, y_grid = np.meshgrid(x_range, y_range)
    z_grid = (-d - a * x_grid - b * y_grid) / c
    # 绘制点和拟合的平面
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="markers",
                marker=dict(size=5),
                name="Points",
            ),
            go.Surface(
                x=x_grid,
                y=y_grid,
                z=z_grid,
                opacity=0.5,
                showscale=False,
                name="Fitted Plane",
            ),
        ]
    )
    # 设置图形布局
    # 设置图形布局
    fig.update_layout(
        width=800,
        height=450,
        autosize=False,
        margin=dict(l=65, r=50, b=65, t=90),
        title="3D Scatter Plot with Plane Equation",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            annotations=[
                dict(
                    showarrow=False,
                    x=0,
                    y=0,
                    z=0,
                    text=f"Plane Equation: {a:.4f}x + {b:.4f}y + {c:.4f}z = {d:.4f}",
                    xanchor="left",
                    xshift=10,
                    opacity=0.7,
                )
            ],
        ),
    )
    return fig


def cal_z(row, a, b, c, d):
    return (-d - a * row["x"] - b * row["y"]) / c


if __name__ == "__main__":
    main()
