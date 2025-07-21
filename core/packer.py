"""
パッキング操作を処理するためのパッカーモジュール
================================================

このモジュールはビンパッキングアルゴリズムの実行と管理を提供します。

Classes:
--------
PackingEngine
    パッキングプロセスを管理するエンジン
"""

from py3dbp import Packer as Py3dbpPacker, Item


class PackingEngine:
    """
    パッキングプロセスを管理するパッキングエンジン。
    
    Attributes:
    -----------
    packer : Py3dbpPacker
        py3dbpのパッカーオブジェクト
    _packed : bool
        パッキングが実行されたかどうかのフラグ
    """
    
    def __init__(self):
        """
        パッキングエンジンを初期化する。
        """
        self.packer = Py3dbpPacker()
        self._packed = False
    
    def add_container(self, container):
        """
        パッカーにコンテナを追加する。
        
        Parameters:
        -----------
        container : Container
            追加するコンテナオブジェクト
        """
        self.packer.add_bin(container.bin)
    
    def add_items(self, items):
        """
        パッカーに複数のアイテムを追加する。
        
        Parameters:
        -----------
        items : list of dict
            アイテムの辞書のリスト。各辞書は以下のキーを含む:
            - name : str - アイテム名
            - width : float - 幅 [mm]
            - height : float - 高さ [mm]
            - depth : float - 奥行き [mm]
            - weight : float - 重量 [g]
            - count : int - 個数
        """
        for item in items:
            for i in range(item["count"]):
                self.packer.add_item(Item(
                    f"{item['name']}_{i}",
                    item["width"],
                    item["height"],
                    item["depth"],
                    item["weight"]
                ))
    
    def pack(self):
        """
        パッキングアルゴリズムを実行する。
        """
        self.packer.pack()
        self._packed = True
    
    @property
    def packed_items(self):
        """
        正常にパックされたアイテムのリストを取得する。
        
        Returns:
        --------
        list
            パックされたアイテムのリスト
        
        Raises:
        -------
        RuntimeError
            pack()が呼ばれていない場合
        """
        if not self._packed:
            raise RuntimeError("Items have not been packed yet. Call pack() first.")
        if len(self.packer.bins) > 0:
            return self.packer.bins[0].items
        return []
    
    @property
    def unfitted_items(self):
        """
        パックできなかったアイテムのリストを取得する。
        
        Returns:
        --------
        list
            パックできなかったアイテムのリスト
        
        Raises:
        -------
        RuntimeError
            pack()が呼ばれていない場合
        """
        if not self._packed:
            raise RuntimeError("Items have not been packed yet. Call pack() first.")
        if len(self.packer.bins) > 0:
            return self.packer.bins[0].unfitted_items
        return []
    
    def get_load_efficiency(self, container):
        """
        積載効率を計算する。
        
        Parameters:
        -----------
        container : Container
            コンテナオブジェクト
            
        Returns:
        --------
        float
            積載効率のパーセンテージ [%]
        """
        if not self._packed:
            return 0.0
        
        used_volume = sum([float(item.width * item.height * item.depth) 
                          for item in self.packed_items])
        return (used_volume / container.volume) * 100
    
    def get_unfitted_stats(self):
        """
        パックできなかったアイテムの統計を取得する。
        
        Returns:
        --------
        dict
            アイテム名をキー、個数を値とする辞書
        """
        stats = {}
        for item in self.unfitted_items:
            item_name = item.name.split('_')[0]
            stats[item_name] = stats.get(item_name, 0) + 1
        return stats