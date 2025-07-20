import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# コンテナのサイズを定義
container_width = 2400
container_height = 2600  
container_depth = 12000

# 3D図を作成
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# コンテナの枠を描画
def draw_container_frame(ax, width, height, depth):
    # 8つの頂点を定義
    vertices = [
        [0, 0, 0],
        [width, 0, 0],
        [width, height, 0],
        [0, height, 0],
        [0, 0, depth],
        [width, 0, depth],
        [width, height, depth],
        [0, height, depth]
    ]
    
    # 12本のエッジを描画
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # 前面
        [4, 5], [5, 6], [6, 7], [7, 4],  # 背面
        [0, 4], [1, 5], [2, 6], [3, 7]   # 側面
    ]
    
    for edge in edges:
        points = [vertices[edge[0]], vertices[edge[1]]]
        ax.plot3D(*zip(*points), 'b-', linewidth=2)

# コンテナの枠を描画
draw_container_frame(ax, container_width, container_height, container_depth)

# 軸の設定
ax.set_xlim([0, container_width])
ax.set_ylim([0, container_height])
ax.set_zlim([0, container_depth])

# ラベルの設定
ax.set_xlabel('Width (mm)')
ax.set_ylabel('Height (mm)')
ax.set_zlabel('Depth (mm)')

# アスペクト比を調整して正しい比率で表示
# 最大値で正規化
max_dim = max(container_width, container_height, container_depth)
ax.set_box_aspect([container_width/max_dim, container_height/max_dim, container_depth/max_dim])

# タイトル
plt.title(f'Container: {container_width} x {container_height} x {container_depth} mm')

# 画像として保存
plt.savefig('results/container_test.png', dpi=150, bbox_inches='tight')
print("Container visualization saved to results/container_test.png")