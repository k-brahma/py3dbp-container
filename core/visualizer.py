"""
パッキング結果の3D可視化のためのビジュアライザーモジュール
==============================================================

このモジュールはパッキング結果の3D可視化機能を提供します。

Classes:
--------
PackingVisualizer
    パッキング結果の3D可視化を作成するクラス
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from .utils import ColorMapper, get_rotated_dimensions


class PackingVisualizer:
    """
    パッキング結果の3D可視化を作成するビジュアライザークラス。
    
    Attributes:
    -----------
    figsize : tuple
        matplotlibの図のサイズ
    color_mapper : ColorMapper
        アイテムの色マッピングを管理するオブジェクト
    """
    
    def __init__(self, figsize=(12, 8)):
        """
        ビジュアライザーを初期化する。
        
        Parameters:
        -----------
        figsize : tuple, optional
            matplotlibの図のサイズ（デフォルト: (12, 8)）
        """
        self.figsize = figsize
        self.color_mapper = ColorMapper()
    
    def visualize(self, container, packing_engine):
        """
        パッキング結果の3D可視化を作成する。
        
        Parameters:
        -----------
        container : Container
            コンテナオブジェクト
        packing_engine : PackingEngine
            パックされたアイテムを持つパッキングエンジンオブジェクト
            
        Returns:
        --------
        tuple
            (fig, ax) matplotlibの図と軸オブジェクトのタプル
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw container frame
        self._draw_container_frame(ax, container)
        
        # Generate color map for items
        color_map = self.color_mapper.generate_color_map(
            packing_engine.packed_items,
            packing_engine.unfitted_items
        )
        
        # Draw packed items
        self._draw_packed_items(ax, packing_engine.packed_items, color_map)
        
        # Set 3D plot properties
        self._setup_3d_plot(ax, container)
        
        return fig, ax
    
    def _draw_container_frame(self, ax, container):
        """
        コンテナの枠を描画する。
        
        Parameters:
        -----------
        ax : Axes3D
            matplotlibの3D軸オブジェクト
        container : Container
            コンテナオブジェクト
        """
        width, height, depth = container.get_dimensions()
        
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
    
    def _draw_cargo_box(self, ax, position, size, color, alpha=0.7):
        """
        単一の貨物ボックスを描画する。
        
        Parameters:
        -----------
        ax : Axes3D
            matplotlibの3D軸オブジェクト
        position : list or tuple
            [x, y, z]形式の位置座標
        size : list or tuple
            [幅, 高さ, 奥行き]形式のサイズ
        color : str
            ボックスの色（16進数カラーコード）
        alpha : float, optional
            透明度（デフォルト: 0.7）
        """
        x, y, z = position
        w, h, d = size
        
        vertices = [
            [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]],
            [[x, y, z + d], [x + w, y, z + d], [x + w, y + h, z + d], [x, y + h, z + d]],
            [[x, y, z], [x, y, z + d], [x + w, y, z + d], [x + w, y, z]],
            [[x, y + h, z], [x, y + h, z + d], [x + w, y + h, z + d], [x + w, y + h, z]],
            [[x, y, z], [x, y, z + d], [x, y + h, z + d], [x, y + h, z]],
            [[x + w, y, z], [x + w, y, z + d], [x + w, y + h, z + d], [x + w, y + h, z]]
        ]
        
        ax.add_collection3d(Poly3DCollection(
            vertices, 
            alpha=alpha, 
            facecolor=color, 
            edgecolor='black', 
            linewidth=0.5
        ))
    
    def _draw_packed_items(self, ax, packed_items, color_map):
        """
        すべてのパックされたアイテムを描画する。
        
        Parameters:
        -----------
        ax : Axes3D
            matplotlibの3D軸オブジェクト
        packed_items : list
            パックされたアイテムのリスト
        color_map : dict
            アイテム名と色のマッピング辞書
        """
        for item in packed_items:
            item_name = item.name.split('_')[0]
            color = color_map.get(item_name, "#999999")
            size = get_rotated_dimensions(item)
            position = [float(item.position[0]), float(item.position[1]), float(item.position[2])]
            self._draw_cargo_box(ax, position, size, color)
    
    def _setup_3d_plot(self, ax, container):
        """
        3Dプロットのプロパティを設定する。
        
        Parameters:
        -----------
        ax : Axes3D
            matplotlibの3D軸オブジェクト
        container : Container
            コンテナオブジェクト
        """
        width, height, depth = container.get_dimensions()
        
        ax.set_xlim([0, float(width)])
        ax.set_ylim([0, float(height)])
        ax.set_zlim([0, float(depth)])
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        
        # Set aspect ratio (normalize by the largest dimension)
        max_dim = max(float(width), float(height), float(depth))
        ax.set_box_aspect([float(width)/max_dim, float(height)/max_dim, float(depth)/max_dim])
        ax.view_init(elev=20, azim=-60)