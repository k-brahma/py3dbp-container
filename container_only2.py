from py3dbp import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# コンテナを作成（幅1500、高さ300、奥行き300）
container = Bin('Container', 1500, 300, 300, 30000)

print(f"Container: width={container.width}, height={container.height}, depth={container.depth}")

# 3D表示
fig = plt.figure(figsize=(14, 6))
ax = fig.add_subplot(111, projection='3d')

# コンテナの枠を描画
vertices = [
    [0, 0, 0],
    [1500, 0, 0],
    [1500, 0, 300],
    [0, 0, 300],
    [0, 300, 0],
    [1500, 300, 0],
    [1500, 300, 300],
    [0, 300, 300]
]

edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
]

for edge in edges:
    points = [vertices[edge[0]], vertices[edge[1]]]
    ax.plot3D(*zip(*points), 'b-', linewidth=2)

ax.set_xlim([0, 1500])
ax.set_ylim([0, 300])
ax.set_zlim([0, 300])
ax.set_xlabel('Width (X)')
ax.set_ylabel('Depth (Y)')
ax.set_zlabel('Height (Z)')

ax.view_init(elev=20, azim=45)

# アスペクト比を実際の比率に設定
ax.set_box_aspect([1500, 300, 300])

plt.title(f'Container: 1500 x 300 x 300 (Width x Height x Depth)')
plt.savefig('results/container_only2.png')
print("Saved to results/container_only2.png")