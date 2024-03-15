import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go

# matplotlib 图形正常显示中文及负号
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
# 二次曲面拟合/leastsq库的使用
###最小二乘法试验###
# error是自定义计算误差的函数，k,b也就是p0是计算初始化值，args是error其余的参数，该函数返回2个值，第一个是k,b的值
from scipy.optimize import leastsq

import numpy as np
import matplotlib.pyplot as plt
import cufflinks as cf

cf.go_offline()


# 拟合曲面函数
def read_data(file_path):
    data = pd.read_csv(file_path, header=[0])

    # plt.show()
    # 假设CSV文件中的数据格式为(x, y, z)
    x = data.loc[:, "x"]
    y = data.loc[:, "y"]
    z = data.loc[:, "z"]
    # trace = go.Surface(x=x, y=y, z=z)
    # data = [trace]
    # layout = go.Layout(title="3D Surface plot")
    # fig = go.Figure(data=data)

    return x, y, z


# 绘制曲面图
def plot_surface(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")
    plt.show()


# 主函数
def main():
    file_path = "coordinates.csv"  # 替换为你的CSV文件路径
    X, Y, Z = read_data(file_path)
    # TEST
    plot_mesh(X, Y, Z)
    p0 = [1, 1, 1, 1, 1, 1]

    # print( error(p0,Xi,Yi) )

    ###主函数从此开始###
    s = "Test the number of iteration"  # 试验最小二乘法函数leastsq得调用几次error函数才能找到使得均方误差之和最小的k、b
    Para = leastsq(error, np.array(p0), args=(X, Y, Z))  # 把error函数中除了p以外的参数打包到args中
    # a, b, c, d, e, f = Para[0]
    print("根据数据点，得到函数f(x,y)=ax^2+by^2+cxy+dx+ey+f的拟合系数依次为：".format(Para[0]))
    # print(Para[0])

    Z1 = func(X, Y, Para[0])
    plot_mesh(X, Y, Z1)
    ###绘图，看拟合效果###


def plot_mesh(X, Y, Z):
    # 使用Seaborn绘制三维曲面图
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    # 创建曲面图
    surf = ax.plot_trisurf(X, Y, Z, cmap="viridis", edgecolor="none")
    # 设置图表标题和轴标签
    ax.set_title("3D Surface Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    # 添加颜色条
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def func(x, y, p):
    return p[0] * x ** 2 + p[1] * y ** 2 + p[2] * x * y + p[3] * x + p[4] * y + p[5]


def error(p, x, y, z):
    return abs(func(x, y, p) - z)  # x、y都是列表，故返回值也是个列表


if __name__ == "__main__":
    main()
