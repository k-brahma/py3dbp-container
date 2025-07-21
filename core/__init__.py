"""
コンテナパッキングアプリケーションのコアパッケージ
==================================================

このパッケージは3Dコンテナパッキング最適化のコア機能を提供します。

モジュール:
-----------
container
    コンテナの仕様と管理
packer
    ビンパッキングアルゴリズムのパッキングエンジン
visualizer
    パッキング結果の3D可視化
utils
    ユーティリティ関数とヘルパークラス

使用例:
-------
コアモジュールの基本的な使用方法::

    from core.container import Container
    from core.packer import PackingEngine
    from core.visualizer import PackingVisualizer
    
    # コンテナの作成
    container = Container(width=1200, height=300, depth=300)
    
    # アイテムのパッキング
    engine = PackingEngine()
    engine.add_container(container)
    engine.add_items(items)
    engine.pack()
    
    # 結果の可視化
    visualizer = PackingVisualizer()
    fig, ax = visualizer.visualize(container, engine)
"""