import numpy as np

from pclpy import pcl


def plane(cloud, normal_vector):
    coeffs = pcl.ModelCoefficients()  # 创建了一个模型系数对象
    coeffs.values.append(normal_vector[0])  # a = 0.0
    coeffs.values.append(normal_vector[1])  # b = 0.0
    coeffs.values.append(normal_vector[2])  # c = 1.0
    coeffs.values.append(normal_vector[3])  # d = 0.0

    # 创建滤波器
    proj = pcl.filters.ProjectInliers.PointXYZ()  # 过滤器对象 proj，用于将点云投影到一个模型上。
    proj.setModelType(0)  # 模型类型被设为 0，代表使用平面模型。
    proj.setInputCloud(cloud)  # 将cloud点云数据进行处理
    proj.setModelCoefficients(coeffs)  # 处理参数coeffs
    cloud_projected = pcl.PointCloud.PointXYZ()  # 建立保存点云
    proj.filter(cloud_projected)  # 将投影结果保存

    return cloud_projected
def compareCloudShow(cloud1, cloud2):
    """
    Args:在一个窗口生成2个窗口可视化点云
        cloud1: 点云数据1
        cloud2: 点云数据2
    """
    viewer = pcl.visualization.PCLVisualizer("viewer")  # 建立可刷窗口对象 窗口名 viewer
    v0 = 1  # 设置标签名（0, 1标记第一个窗口）
    viewer.createViewPort(0.0, 0.0, 0.5, 1.0, v0)  # 创建一个可视化的窗口
    viewer.setBackgroundColor(0.0, 0.0, 0.0, v0)  # 设置窗口背景为黑色
    single_color = pcl.visualization.PointCloudColorHandlerCustom.PointXYZ(cloud1, 255.0, 0, 0.0)  # 将点云设置为红色
    viewer.addPointCloud(cloud1,          # 要添加到窗口的点云数据。
                         single_color,    # 指定点云的颜色
                         "sample cloud1",  # 添加的点云命名
                         v0)  # 点云添加到的视图

    v1 = 2  # 设置标签名（2代表第二个窗口）
    viewer.createViewPort(0.5, 0.0, 1.0, 1.0, v1)  # 创建一个可视化的窗口
    viewer.setBackgroundColor(255.0, 255.0, 255.0, v1)  # 设置窗口背景为白色
    single_color = pcl.visualization.PointCloudColorHandlerCustom.PointXYZ(cloud2, 0.0, 255.0, 0.0)  # 将点云设置为绿色
    viewer.addPointCloud(cloud2,  # 要添加到窗口的点云数据。
                         single_color,  # 指定点云的颜色
                         "sample cloud2",  # 添加的点云命名
                         v1)  # 点云添加到的视图

    # 设置点云窗口（可移除对点云可视化没有影响）
    viewer.setPointCloudRenderingProperties(0,  # 设置点云点的大小
                                            1,  # 点云像素
                                            "sample cloud1",  # 识别特定点云
                                            v0)  # 在那个窗口可视化
    viewer.setPointCloudRenderingProperties(0,  # 设置点云点的大小
                                            1,  # 点云像素
                                            "sample cloud2",  # 识别特定点云
                                            v1)  # 在那个窗口可视化
    # viewer.addCoordinateSystem(1.0)  # 设置坐标轴 坐标轴的长度为1.0
    # 窗口建立
    while not viewer.wasStopped():
        viewer.spinOnce(10)

if __name__ == '__main__':
    """ 拟合出的平面方程为： ax + by +cz + d = 0"""
    """约束条件 a^2 + b^2 + c^2 = 1"""
    cloud1 = pcl.PointCloud.PointXYZ()
    reader = pcl.io.PCDReader()  # 设置读取对象
    reader.read('res/bunny.pcd', cloud1)  # 读取点云保存在cloud中
    points = cloud1.xyz
    # 获得平均值
    avg_x = np.mean(points[:, 0])
    avg_y = np.mean(points[:, 1])
    avg_z = np.mean(points[:, 2])

    # 去重心化
    x = points[:, 0] - avg_x
    y = points[:, 1] - avg_y
    z = points[:, 2] - avg_z
    # 生成矩阵
    A = np.transpose(np.asarray([x, y, z]))  # 将数据矩阵化

    """AX = 0"""
    # 计算协方差矩阵
    cov_matrix = np.cov(A, rowvar=False)

    # 使用 SVD 分解求解协方差矩阵的特征值和特征向量
    U, S, Vt = np.linalg.svd(cov_matrix)

    # 特征值和特征向量
    eigenvalues = S
    eigenvectors = Vt.T  # 转置后得到正确的特征向量 一行代表一个特征向量 最小的特征向量在最后一行

    print("特征值：", eigenvalues)
    print("特征向量：", eigenvectors)

    """如果想要找到最小的特征向量，可以直接从特征向量矩阵中取最后一列（没有转置前），
    因为特征向量是按特征值从大到小排列的，所以最后一列就是对应最小特征值的特征向量。"""
    X = eigenvectors[2]
    center =  np.mean(points, axis=0)  # 获得中心（质心）质心是一个几何概念，通常用于描述几何图形（如点集、线段、多边形等）的中心位置。
    print('平面拟合结果为：0 = %.3f * x + %.3f * y + %.3f + %3.f' % (
    X[0], X[1], X[2], (-X[0] * center[0] - X[1] * center[1] - X[2] * center[2])))
    plane_cloud = plane(cloud1,
                        (X[0], X[1], X[2], (-X[0] * center[0] - X[1] * center[1] - X[2] * center[2])))  # 获得投影后的点云数据
    # ------------------ 可视化点云 -----------------
    compareCloudShow(cloud1, plane_cloud)
