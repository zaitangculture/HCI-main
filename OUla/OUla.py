import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R

def plot_cube(ax, rotation_matrix, color='cyan', alpha=0.5):
    # 定义立方体的8个顶点
    vertices = np.array([[0, 0, 0],
                         [1, 0, 0],
                         [1, 1, 0],
                         [0, 1, 0],
                         [0, 0, 1],
                         [1, 0, 1],
                         [1, 1, 1],
                         [0, 1, 1]])

    # 定义立方体的12个面（每个面由4个顶点组成）
    faces = [[vertices[j] for j in [0, 1, 2, 3]],
             [vertices[j] for j in [4, 5, 6, 7]],
             [vertices[j] for j in [0, 1, 5, 4]],
             [vertices[j] for j in [2, 3, 7, 6]],
             [vertices[j] for j in [0, 3, 7, 4]],
             [vertices[j] for j in [1, 2, 6, 5]]]

    # 应用旋转矩阵到顶点
    rotated_vertices = np.dot(vertices, rotation_matrix.T)

    # 绘制立方体
    poly3d = Poly3DCollection(faces, color=color, alpha=alpha)
    ax.add_collection3d(poly3d)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])

# 定义欧拉角（绕z, y', x''的旋转角度）
euler_angles = [45, 30, 60]  # 角度值

# 创建旋转对象
r = R.from_euler('zyx', euler_angles, degrees=True)

# 获取旋转矩阵
rotation_matrix = r.as_matrix()

# 创建图形
fig = plt.figure(figsize=(12, 6))

# 绘制原始立方体
ax1 = fig.add_subplot(121, projection='3d')
plot_cube(ax1, np.eye(3), color='cyan', alpha=0.5)
ax1.set_title('Original Cube')

# 绘制旋转后的立方体
ax2 = fig.add_subplot(122, projection='3d')
plot_cube(ax2, rotation_matrix, color='orange', alpha=0.5)
ax2.set_title('Rotated Cube')

plt.show()
