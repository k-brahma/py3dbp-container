"""
コンテナ仕様を管理するためのコンテナモジュール
==============================================

このモジュールはコンテナの仕様定義と操作を提供します。

Classes:
--------
Container
    コンテナの仕様と操作を管理するクラス
"""

from py3dbp import Bin


class Container:
    """
    コンテナの仕様と操作を管理するクラス。
    
    Attributes:
    -----------
    name : str
        コンテナの名前
    width : float
        コンテナの幅（X軸方向）[m]
    height : float
        コンテナの高さ（Y軸方向）[m]
    depth : float
        コンテナの奥行き（Z軸方向）[m]
    max_weight : float
        最大積載重量 [kg]
    """
    
    def __init__(self, name='Container', width=12.03, height=2.39, depth=2.35, max_weight=28000):
        """
        指定された寸法でコンテナを初期化する。
        
        Parameters:
        -----------
        name : str, optional
            コンテナの名前（デフォルト: 'Container'）
        width : float, optional
            コンテナの幅 [m]（デフォルト: 12.03 - 40フィートコンテナ）
        height : float, optional
            コンテナの高さ [m]（デフォルト: 2.39）
        depth : float, optional
            コンテナの奥行き [m]（デフォルト: 2.35）
        max_weight : float, optional
            最大積載重量 [kg]（デフォルト: 28000）
        """
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self._bin = None
    
    def create_bin(self):
        """
        py3dbp Binオブジェクトを作成して返す。
        
        Returns:
        --------
        Bin
            py3dbpのBinオブジェクト
        """
        self._bin = Bin(self.name, self.width, self.height, self.depth, self.max_weight)
        return self._bin
    
    @property
    def bin(self):
        """
        py3dbp Binオブジェクトを取得する。
        
        必要に応じて作成される。
        
        Returns:
        --------
        Bin
            py3dbpのBinオブジェクト
        """
        if self._bin is None:
            self.create_bin()
        return self._bin
    
    @property
    def volume(self):
        """
        コンテナの容積を計算して返す。
        
        Returns:
        --------
        float
            コンテナの容積 [m³]
        """
        return float(self.width * self.height * self.depth)
    
    def get_dimensions(self):
        """
        コンテナの寸法をタプルとして返す。
        
        Returns:
        --------
        tuple
            (幅, 高さ, 奥行き) の形式の寸法タプル
        """
        return (self.width, self.height, self.depth)
    
    def __str__(self):
        """
        コンテナの文字列表現。
        
        Returns:
        --------
        str
            コンテナの情報を含む文字列
        """
        return f"Container({self.name}): {self.width}x{self.height}x{self.depth}m, max_weight={self.max_weight}kg"