from py3dbp import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os
from datetime import datetime

# resultsディレクトリを作成
os.makedirs('results', exist_ok=True)

def create_container():
    """コンテナを作成する関数"""
    # Bin(name, width(x), height(y), depth(z), max_weight)
    # 細長い直方体: X方向に1200mm
    return Bin('Container', 1200, 300, 300, 30000)

def create_cargo_items():
    """貨物アイテムを定義する関数"""
    return [
        {"name": "small", "width": 100, "height": 100, "depth": 100, "weight": 20, "count": 12},
        {"name": "medium", "width": 150, "height": 100, "depth": 80, "weight": 30, "count": 10},
        {"name": "large", "width": 200, "height": 150, "depth": 100, "weight": 40, "count": 4},
        {"name": "item5", "width": 160, "height": 140, "depth": 90, "weight": 35, "count": 8},
        {"name": "item6", "width": 120, "height": 80, "depth": 80, "weight": 25, "count": 10}
    ]

def pack_items(container, items):
    """アイテムをコンテナにパッキングする関数"""
    packer = Packer()
    packer.add_bin(container)
    
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
    return packer

def draw_container_frame(ax, width, height, depth):
    """コンテナの枠を描画する関数"""
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
    
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    
    for edge in edges:
        points = [vertices[edge[0]], vertices[edge[1]]]
        ax.plot3D(*zip(*points), 'b-', linewidth=2)

def draw_cargo_box(ax, pos, size, color, alpha=0.7):
    """貨物ボックスを描画する関数"""
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
    
    ax.add_collection3d(Poly3DCollection(vertices, alpha=alpha, facecolor=color, edgecolor='black', linewidth=0.5))

def visualize_packing(container, packer):
    """パッキング結果を可視化する関数"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # コンテナの枠を描画
    draw_container_frame(ax, float(container.width), float(container.height), float(container.depth))
    
    # 色のマッピング
    color_map = {
        "small": "#FF6B6B",
        "medium": "#4ECDC4",
        "large": "#45B7D1",
        "xlarge": "#96CEB4",
        "item5": "#FECA57",
        "item6": "#DDA0DD"
    }
    
    # 配置された貨物を描画
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
            
            draw_cargo_box(ax, [float(item.position[0]), float(item.position[1]), float(item.position[2])], 
                          size, color)
    
    ax.set_xlim([0, float(container.width)])
    ax.set_ylim([0, float(container.height)])
    ax.set_zlim([0, float(container.depth)])
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    
    # アスペクト比を正しく設定
    ax.set_box_aspect([float(container.width)/300, float(container.height)/300, float(container.depth)/300])
    
    ax.view_init(elev=20, azim=-60)
    
    return fig, ax

def print_packing_results(container, packer):
    """パッキング結果を出力する関数"""
    print(f"Container: width={container.width}, height={container.height}, depth={container.depth}")
    print(f"\nFitted items: {len(packer.bins[0].items)}")
    print(f"Unfitted items: {len(packer.bins[0].unfitted_items)}")
    
    # 効率計算
    total_container_volume = float(container.width * container.height * container.depth)
    used_volume = sum([float(item.width * item.height * item.depth) for item in packer.bins[0].items])
    load_efficiency = (used_volume / total_container_volume) * 100
    print(f"\nLoad efficiency: {load_efficiency:.1f}%")
    
    # 配置されたアイテムの詳細
    print("\n===== Packed items =====")
    for item in packer.bins[0].items:
        print(f"  {item.string()}: position = {item.position}, rotation_type = {item.rotation_type}")
    
    if packer.bins[0].unfitted_items:
        print("\n===== Unfitted items =====")
        for item in packer.bins[0].unfitted_items:
            print(f"  {item.string()}")
    
    return load_efficiency

# メイン処理
if __name__ == "__main__":
    # コンテナを作成
    container = create_container()
    
    # 貨物アイテムを作成
    items = create_cargo_items()
    
    # パッキングを実行
    packer = pack_items(container, items)
    
    # 結果を出力
    load_efficiency = print_packing_results(container, packer)
    
    # 可視化
    fig, ax = visualize_packing(container, packer)

    # タイトルと保存
    plt.title(f'Container Packing: {container.width} x {container.height} x {container.depth}\nLoad Efficiency: {load_efficiency:.1f}%')
    
    # タイムスタンプを付けて保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f'results/container_with_cargo_{timestamp}.png', dpi=150, bbox_inches='tight')
    print(f"\nSaved to results/container_with_cargo_{timestamp}.png")
    plt.show()