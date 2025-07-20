from py3dbp import *

def create_container(width=1500, height=300, depth=300, max_weight=30000, name='Container'):
    """
    コンテナを作成する関数
    
    Args:
        width: コンテナの幅 (mm) デフォルト: 1500
        height: コンテナの高さ (mm) デフォルト: 300
        depth: コンテナの奥行き (mm) デフォルト: 300
        max_weight: 最大重量 (kg) デフォルト: 30000
        name: コンテナの名前 デフォルト: 'Container'
    
    Returns:
        Bin: 作成されたコンテナオブジェクト
    """
    container = Bin(name, width, height, depth, max_weight)
    return container


# テスト用
if __name__ == "__main__":
    # デフォルト値でコンテナを作成
    container1 = create_container()
    print(f"Default container: {container1.width} x {container1.height} x {container1.depth}")
    
    # カスタムサイズでコンテナを作成
    container2 = create_container(width=2000, height=400, depth=600, name='Large Container')
    print(f"Custom container: {container2.width} x {container2.height} x {container2.depth}")