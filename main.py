from py3dbp import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os
from datetime import datetime
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# resultsディレクトリを作成
os.makedirs('results', exist_ok=True)

# コンテナの設定（名前、幅、高さ、奥行き、最大重量）
# 細長い直方体: 幅300mm x 高さ300mm x 奥行き1500mm (奥行きが5倍)
container = Bin('Container', 300, 300, 1500, 30000)

# パッカーの作成
packer = Packer()
packer.add_bin(container)

# アイテムの定義（名前、幅、奥、高さ、重量、個数）
items = [
    {"name": "small", "width": 50, "height": 50, "depth": 50, "weight": 10, "count": 3},
    {"name": "medium", "width": 75, "height": 25, "depth": 50, "weight": 15, "count": 2},
    {"name": "large", "width": 100, "height": 50, "depth": 50, "weight": 20, "count": 1},
    {"name": "xlarge", "width": 25, "height": 75, "depth": 100, "weight": 25, "count": 2},
    {"name": "item5", "width": 80, "height": 60, "depth": 40, "weight": 18, "count": 3},
    {"name": "item6", "width": 30, "height": 45, "depth": 35, "weight": 7, "count": 4}
]

# 新しいビンニング問題に対する準備 == 
total_item_volume = sum([item["width"] * item["height"] * item["depth"] * item["count"] for item in items])
total_container_volume = float(container.width * container.height * container.depth)
max_load_efficiency = (total_item_volume / total_container_volume) * 100

print("Adding items...")

# アイテムをパッカーに追加
for item in items:
    for i in range(item["count"]):
        packer.add_item(Item(
            f"{item['name']}_{i}", 
            item["width"], 
            item["height"], 
            item["depth"], 
            item["weight"]
        ))

# パッキングを実行
packer.pack()

# 結果の出力
result_text = []
for i, b in enumerate(packer.bins):
    result_text.append(f"\n===== {b.string()} =====")
    result_text.append(f"Fitted items: {len(b.items)}")
    result_text.append(f"Unfitted items: {len(b.unfitted_items)}")
    
    for item in b.items:
        result_text.append(f"  {item.string()}: position = {item.position}, rotation_type = {item.rotation_type}")
    
    for item in b.unfitted_items:
        result_text.append(f"  Unfitted: {item.string()}")
    
    # 効率計算
    used_volume = sum([float(item.width * item.height * item.depth) for item in b.items])
    load_efficiency = (used_volume / total_container_volume) * 100
    result_text.append(f"\nLoad efficiency: {load_efficiency:.1f}%")

# 結果をコンソールに出力
for line in result_text:
    print(line)

# 結果をファイルに保存
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f'results/packing_result_{timestamp}.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result_text))

# 3Dビジュアライゼーション
def draw_box(ax, pos, size, color):
    x, y, z = pos
    w, h, d = size
    
    vertices = [
        [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]],
        [[x, y, z + d], [x + w, y, z + d], [x + w, y + h, z + d], [x, y + h, z + d]],
        [[x, y, z], [x, y, z + d], [x + w, y, z + d], [x + w, y, z]],
        [[x, y + h, z], [x, y + h, z + d], [x + w, y + h, z + d], [x + w, y + h, z]],
        [[x, y, z], [x, y, z + d], [x, y + h, z + d], [x, y + h, z]],
        [[x + w, y, z], [x + w, y, z + d], [x + w, y + h, z + d], [x + w, y + h, z]]
    ]
    
    ax.add_collection3d(Poly3DCollection(vertices, alpha=0.7, facecolor=color, edgecolor='black', linewidth=0.5))

# コンテナの可視化
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 視点を調整（elevation=20度、azimuth=45度）
ax.view_init(elev=20, azim=45)

# 3Dプロットの設定
ax.set_xlim([0, float(container.width)])
ax.set_ylim([0, float(container.height)])
ax.set_zlim([0, float(container.depth)])
ax.set_xlabel('Width (mm)')
ax.set_ylabel('Height (mm)')
ax.set_zlabel('Depth (mm)')

# アスペクト比を調整して正しい比率で表示
max_dim = max(float(container.width), float(container.height), float(container.depth))
ax.set_box_aspect([float(container.width)/max_dim, float(container.height)/max_dim, float(container.depth)/max_dim])

# 色のマッピング
color_map = {
    "small": "#FF6B6B",
    "medium": "#4ECDC4",
    "large": "#45B7D1",
    "xlarge": "#96CEB4",
    "item5": "#FECA57",
    "item6": "#DDA0DD"
}

# 配置されたアイテムを描画
if len(packer.bins) > 0 and len(packer.bins[0].items) > 0:
    for item in packer.bins[0].items:
        item_name = item.name.split('_')[0]
        color = color_map.get(item_name, "#999999")
        
        # rotation_typeに基づいて寸法を調整
        if item.rotation_type == 0:  # WHD
            size = [float(item.width), float(item.height), float(item.depth)]
        elif item.rotation_type == 1:  # HWD
            size = [float(item.height), float(item.width), float(item.depth)]
        elif item.rotation_type == 2:  # HDW
            size = [float(item.height), float(item.depth), float(item.width)]
        elif item.rotation_type == 3:  # DHW
            size = [float(item.depth), float(item.height), float(item.width)]
        elif item.rotation_type == 4:  # DWH
            size = [float(item.depth), float(item.width), float(item.height)]
        elif item.rotation_type == 5:  # WDH
            size = [float(item.width), float(item.depth), float(item.height)]
        
        draw_box(ax, [float(item.position[0]), float(item.position[1]), float(item.position[2])], 
                 size, color)

# タイトルと効率を表示
if len(packer.bins) > 0:
    used_volume = sum([float(item.width * item.height * item.depth) for item in packer.bins[0].items])
    load_efficiency = (used_volume / total_container_volume) * 100
else:
    load_efficiency = 0

plt.title(f'Container Packing Optimization Result\nLoad Efficiency: {load_efficiency:.1f}%')

# 画像を保存
plt.savefig(f'results/packing_visualization_{timestamp}.png', dpi=150, bbox_inches='tight')
plt.show()