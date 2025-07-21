"""
コンテナパッキングアプリケーションのメインクラスベース実装
==============================================================

このモジュールはコンテナパッキングアプリケーションのメインエントリーポイントを提供します。

Classes:
--------
ContainerPackingApp
    コンテナパッキングのメインアプリケーションクラス

Functions:
----------
main
    アプリケーションを実行するメイン関数

使用例:
-------
基本的な使用方法::

    app = ContainerPackingApp()
    app.run(item_set='japanese')

カスタム設定での使用::

    app = ContainerPackingApp()
    app.run(
        container_dims={'width': 1500, 'height': 400, 'depth': 400},
        item_set='test'
    )
"""

import os
from datetime import datetime
import matplotlib.pyplot as plt

from core.container import Container
from core.packer import PackingEngine
from core.visualizer import PackingVisualizer
from core.utils import ColorMapper, ResultPrinter
from cargo_items import create_cargo_items, create_test_cargo_items, create_japanese_cargo_items


class ContainerPackingApp:
    """
    コンテナパッキングのメインアプリケーションクラス。
    
    Attributes:
    -----------
    results_dir : str
        結果を保存するディレクトリ
    container : Container
        コンテナオブジェクト
    packing_engine : PackingEngine
        パッキングエンジンオブジェクト
    visualizer : PackingVisualizer
        可視化オブジェクト
    color_mapper : ColorMapper
        色マッピングオブジェクト
    """
    
    def __init__(self, results_dir='results'):
        """
        コンテナパッキングアプリケーションを初期化する。
        
        Parameters:
        -----------
        results_dir : str, optional
            結果を保存するディレクトリ（デフォルト: 'results'）
        """
        self.results_dir = results_dir
        self.container = None
        self.packing_engine = None
        self.visualizer = PackingVisualizer()
        self.color_mapper = ColorMapper()
        
        # Create results directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)
    
    def setup_container(self, width=12.03, height=2.39, depth=2.35, max_weight=28000):
        """
        指定された寸法でコンテナを設定する。
        
        Parameters:
        -----------
        width : float, optional
            コンテナの幅 [m]（デフォルト: 12.03 - 40フィートコンテナ）
        height : float, optional
            コンテナの高さ [m]（デフォルト: 2.39）
        depth : float, optional
            コンテナの奥行き [m]（デフォルト: 2.35）
        max_weight : float, optional
            最大積載重量 [kg]（デフォルト: 28000）
        """
        self.container = Container('Container', width, height, depth, max_weight)
    
    def load_items(self, item_set='japanese'):
        """
        指定されたセットに基づいて貨物アイテムを読み込む。
        
        Parameters:
        -----------
        item_set : str, optional
            読み込むアイテムのタイプ（'japanese', 'test', 'default'）
            （デフォルト: 'japanese'）
            
        Returns:
        --------
        list
            アイテム辞書のリスト
        """
        if item_set == 'japanese':
            return create_japanese_cargo_items()
        elif item_set == 'test':
            return create_test_cargo_items()
        else:
            return create_cargo_items()
    
    def pack_items(self, items):
        """
        アイテムをコンテナにパックする。
        
        Parameters:
        -----------
        items : list
            アイテム辞書のリスト
            
        Raises:
        -------
        RuntimeError
            コンテナが設定されていない場合
        """
        if not self.container:
            raise RuntimeError("Container not set up. Call setup_container() first.")
        
        self.packing_engine = PackingEngine()
        self.packing_engine.add_container(self.container)
        self.packing_engine.add_items(items)
        self.packing_engine.pack()
    
    def visualize_results(self):
        """
        パッキング結果の可視化を作成する。
        
        Returns:
        --------
        tuple
            (fig, ax) matplotlibの図と軸オブジェクトのタプル
            
        Raises:
        -------
        RuntimeError
            パッキング結果がない場合
        """
        if not self.packing_engine:
            raise RuntimeError("No packing results to visualize. Call pack_items() first.")
        
        return self.visualizer.visualize(self.container, self.packing_engine)
    
    def print_results(self):
        """
        詳細なパッキング結果を出力する。
        
        Returns:
        --------
        float
            積載効率のパーセンテージ [%]
            
        Raises:
        -------
        RuntimeError
            パッキング結果がない場合
        """
        if not self.packing_engine:
            raise RuntimeError("No packing results to print. Call pack_items() first.")
        
        color_map = self.color_mapper.generate_color_map(
            self.packing_engine.packed_items,
            self.packing_engine.unfitted_items
        )
        
        return ResultPrinter.print_results(self.container, self.packing_engine, color_map)
    
    def save_visualization(self, fig, title=None):
        """
        可視化をファイルに保存する。
        
        Parameters:
        -----------
        fig : Figure
            Matplotlibの図オブジェクト
        title : str, optional
            プロットのオプションタイトル
            
        Returns:
        --------
        str
            保存されたファイルのパス
        """
        if title:
            plt.title(title)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{self.results_dir}/container_with_cargo_{timestamp}.png'
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"\nSaved to {filename}")
        return filename
    
    def run(self, container_dims=None, item_set='japanese', show_plot=True):
        """
        完全なパッキングプロセスを実行する。
        
        Parameters:
        -----------
        container_dims : dict, optional
            オプションのコンテナ寸法
        item_set : str, optional
            読み込むアイテムのタイプ（デフォルト: 'japanese'）
        show_plot : bool, optional
            プロットを表示するかどうか（デフォルト: True）
        """
        # Setup container
        if container_dims:
            self.setup_container(**container_dims)
        else:
            self.setup_container()
        
        # Load and pack items
        items = self.load_items(item_set)
        self.pack_items(items)
        
        # Print results
        efficiency = self.print_results()
        
        # Visualize
        fig, ax = self.visualize_results()
        
        # Add title and save
        title = (f'Container Packing: {self.container.width} x {self.container.height} x {self.container.depth}\n'
                f'Load Efficiency: {efficiency:.1f}%')
        self.save_visualization(fig, title)
        
        if show_plot:
            plt.show()


def main():
    """
    アプリケーションを実行するメイン関数。
    """
    app = ContainerPackingApp()
    
    # Run with default settings
    app.run(item_set='japanese')
    
    # Example of running with custom container dimensions
    # app.run(
    #     container_dims={'width': 1500, 'height': 400, 'depth': 400, 'max_weight': 40000},
    #     item_set='test'
    # )


if __name__ == "__main__":
    main()