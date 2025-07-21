"""
コンテナパッキングアプリケーションのためのユーティリティ関数とクラス
==================================================================

このモジュールはアプリケーション全体で使用されるユーティリティを提供します。

Classes:
--------
ColorMapper
    アイテム名を色にマッピングするクラス
ResultPrinter
    パッキング結果の出力を処理するクラス

Functions:
----------
get_rotated_dimensions
    回転タイプに基づいてアイテムの寸法を取得する
"""


class ColorMapper:
    """
    可視化のためにアイテム名を色にマッピングするクラス。
    
    Attributes:
    -----------
    base_colors : dict
        デフォルトのアイテム名と色のマッピング
    available_colors : list
        使用可能な色のリスト
    """
    
    def __init__(self):
        """
        デフォルトの色マッピングで初期化する。
        """
        self.base_colors = {
            "small": "#FF6B6B",
            "medium": "#4ECDC4",
            "large": "#45B7D1",
            "xlarge": "#96CEB4",
            "item5": "#FECA57",
            "item6": "#DDA0DD"
        }
        
        self.available_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#DDA0DD",
            "#FF9FF3", "#54A0FF", "#5F27CD", "#00D2D3", "#FF9F43", "#10AC84",
            "#EE5A24", "#A55EEA", "#26DE81", "#778CA3", "#F8B500", "#FC427B"
        ]
    
    def generate_color_map(self, packed_items, unfitted_items):
        """
        すべてのアイテムに対して色マップを生成する。
        
        Parameters:
        -----------
        packed_items : list
            パックされたアイテムのリスト
        unfitted_items : list
            パックされなかったアイテムのリスト
            
        Returns:
        --------
        dict
            アイテム名と色のマッピング辞書
        """
        color_map = self.base_colors.copy()
        
        # Collect all unique item names
        all_item_names = set()
        for item in packed_items:
            all_item_names.add(item.name.split('_')[0])
        for item in unfitted_items:
            all_item_names.add(item.name.split('_')[0])
        
        # Assign colors to new items
        color_index = len(self.base_colors)
        for item_name in all_item_names:
            if item_name not in color_map:
                color_map[item_name] = self.available_colors[color_index % len(self.available_colors)]
                color_index += 1
        
        return color_map


def get_rotated_dimensions(item):
    """
    回転タイプに基づいてアイテムの寸法を取得する。
    
    Parameters:
    -----------
    item : Item
        rotation_type属性を持つアイテムオブジェクト
        
    Returns:
    --------
    list
        回転後の[幅, 高さ, 奥行き]のリスト
    """
    rotation_map = {
        0: [float(item.width), float(item.height), float(item.depth)],   # WHD
        1: [float(item.height), float(item.width), float(item.depth)],   # HWD
        2: [float(item.height), float(item.depth), float(item.width)],   # HDW
        3: [float(item.depth), float(item.height), float(item.width)],   # DHW
        4: [float(item.depth), float(item.width), float(item.height)],   # DWH
        5: [float(item.width), float(item.depth), float(item.height)]    # WDH
    }
    return rotation_map.get(item.rotation_type, [float(item.width), float(item.height), float(item.depth)])


class ResultPrinter:
    """
    パッキング結果の出力を処理するクラス。
    """
    
    @staticmethod
    def print_results(container, packing_engine, color_map):
        """
        詳細なパッキング結果を出力する。
        
        Parameters:
        -----------
        container : Container
            コンテナオブジェクト
        packing_engine : PackingEngine
            パッキングエンジンオブジェクト
        color_map : dict
            アイテム名と色のマッピング辞書
            
        Returns:
        --------
        float
            積載効率のパーセンテージ [%]
        """
        print(f"Container: width={container.width}, height={container.height}, depth={container.depth}")
        print(f"\nFitted items: {len(packing_engine.packed_items)}")
        print(f"Unfitted items: {len(packing_engine.unfitted_items)}")
        
        # Efficiency
        efficiency = packing_engine.get_load_efficiency(container)
        print(f"\nLoad efficiency: {efficiency:.1f}%")
        
        # Color legend
        print("\n===== Color Legend =====")
        for item_name, color in color_map.items():
            print(f"  {item_name}: {color}")
        
        # Packed items details
        print("\n===== Packed items =====")
        for item in packing_engine.packed_items:
            print(f"  {item.string()}: position = {item.position}, rotation_type = {item.rotation_type}")
        
        # Unfitted items
        if packing_engine.unfitted_items:
            print("\n===== Unfitted items =====")
            unfitted_stats = packing_engine.get_unfitted_stats()
            
            print("積みきれなかったアイテム:")
            for item_name, count in unfitted_stats.items():
                print(f"  {item_name}: {count}個")
            
            print("\n詳細:")
            for item in packing_engine.unfitted_items:
                item_name = item.name.split('_')[0]
                print(f"  {item_name}: {item.string()}")
        else:
            print("\n===== Unfitted items =====")
            print("  積みきれないアイテムはありません")
        
        return efficiency