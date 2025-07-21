# コンテナパッキングアプリケーション

3Dビンパッキングアルゴリズムを使用して、貨物を効率的にコンテナに配置するPythonアプリケーションです。

## 概要

このアプリケーションは、様々なサイズの貨物アイテムを指定されたコンテナに最適に配置する問題を解決します。3D空間での配置を計算し、結果を視覚的に表示します。

### 主な機能

- 🎯 3Dビンパッキングアルゴリズムによる最適配置
- 📊 配置結果の3D可視化
- 📈 積載効率の計算と表示
- 🎨 アイテムごとの色分け表示
- 💾 結果の画像保存
- 🔧 実際の40フィートコンテナサイズに対応（12.03m × 2.39m × 2.35m）

## インストール

### 必要条件

- Python 3.7以上
- pip

### 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方

### 基本的な使用方法

#### 1. GUI アプリケーション（推奨）

```bash
python gui.py
```

GUIでは以下の機能が利用できます：
- 貨物の登録・編集・削除
- CSVファイルのインポート/エクスポート
- コンテナサイズのカスタマイズ
- パッキング結果の3D表示
- pandas DataFrameによる貨物データ管理

#### 2. コマンドライン実行

```bash
python main_class.py
```

### プログラムでの使用

```python
from main_class import ContainerPackingApp

# アプリケーションの初期化
app = ContainerPackingApp()

# デフォルト設定で実行
app.run(item_set='japanese')

# カスタムコンテナサイズで実行
app.run(
    container_dims={
        'width': 1500,
        'height': 400,
        'depth': 400,
        'max_weight': 40000
    },
    item_set='test'
)
```

## プロジェクト構造

```
container-app/
├── core/                    # コアモジュール
│   ├── __init__.py         # パッケージ初期化
│   ├── container.py        # コンテナクラス
│   ├── packer.py          # パッキングエンジン
│   ├── visualizer.py      # 3D可視化
│   ├── interactive_visualizer.py  # インタラクティブ3D可視化
│   └── utils.py           # ユーティリティ関数
├── sample_data/            # サンプル貨物データ（CSV）
│   ├── color_cargo_items.csv    # 色名の貨物
│   ├── test_cargo_items.csv     # テスト用貨物
│   └── japanese_cargo_items.csv # 日本語名の貨物
├── results/                # 出力画像の保存先
├── cargo_items.py         # 貨物データ読み込み（CSVから）
├── gui.py                 # GUIアプリケーション
├── main_class.py         # クラスベースの実装
├── requirements.txt      # 依存パッケージ
└── README.md            # このファイル
```

## 貨物アイテムの設定

貨物データは`sample_data/`ディレクトリのCSVファイルから読み込まれます：

### CSVファイル形式
すべてのCSVファイルは以下のカラムを持つ必要があります：
- `名前` - 貨物の名前
- `幅(m)` - 幅（メートル）
- `高さ(m)` - 高さ（メートル）
- `奥行き(m)` - 奥行き（メートル）
- `重量(kg)` - 重量（キログラム）
- `個数` - 個数

※ 古い形式（mm/g単位）のCSVファイルも自動的にメートル/キログラムに変換されます。

### 提供されているサンプルデータ

1. **日本語名の貨物** (`sample_data/japanese_cargo_items.csv`)
   - 標準パレット貨物、大型パレット貨物、小型コンテナ、中型コンテナ、大型機械、特殊貨物
   - 実際の物流で使用される現実的なサイズ

2. **テスト用貨物** (`sample_data/test_cargo_items.csv`)
   - small_pallet, medium_pallet, large_pallet, industrial_box, machinery
   - 英語名での産業用貨物

3. **色名貨物** (`sample_data/color_cargo_items.csv`)
   - 赤貨物、青貨物、緑貨物、黄貨物、紫貨物
   - デモンストレーション用の色分けされた貨物

### カスタム貨物データの追加
1. `sample_data/`ディレクトリに新しいCSVファイルを作成
2. 上記のカラム形式に従ってデータを入力
3. GUIの「CSVインポート」機能を使用して読み込み

## カスタマイズ

### コンテナサイズの変更

```python
app = ContainerPackingApp()

# 40フィートコンテナ（デフォルト）
app.setup_container(
    width=12.03,     # 幅 [m]
    height=2.39,     # 高さ [m]
    depth=2.35,      # 奥行き [m]
    max_weight=28000 # 最大重量 [kg]
)

# 20フィートコンテナの例
app.setup_container(
    width=5.9,       # 幅 [m]
    height=2.39,     # 高さ [m]
    depth=2.35,      # 奥行き [m]
    max_weight=21000 # 最大重量 [kg]
)
```

### 新しい貨物アイテムの追加

CSVファイルを作成して`sample_data/`に配置：

```csv
名前,幅(m),高さ(m),奥行き(m),重量(kg),個数
カスタムパレット,1.5,1.8,1.2,1200,8
特殊機械,3.0,2.0,2.0,3000,2
```

## 出力

### コンソール出力
- コンテナの仕様
- 配置されたアイテム数と配置できなかったアイテム数
- 積載効率（パーセンテージ）
- 色の凡例
- 各アイテムの詳細な配置情報

### 画像出力
- 3D可視化画像が`results/`ディレクトリに保存されます
- ファイル名: `container_with_cargo_YYYYMMDD_HHMMSS.png`

## API ドキュメント

各モジュールとクラスは詳細なdocstringを含んでいます。主要なクラス：

### `Container`
コンテナの仕様を管理するクラス

### `PackingEngine`
ビンパッキングアルゴリズムを実行するエンジン

### `PackingVisualizer`
3D可視化を生成するクラス

### `ContainerPackingApp`
アプリケーション全体を統括するメインクラス

## トラブルシューティング

### ModuleNotFoundError: No module named 'py3dbp'
```bash
pip install py3dbp
```

### matplotlib の表示に関する問題
環境によっては、GUIウィンドウが表示されない場合があります。その場合は：
```python
app.run(show_plot=False)  # プロットを表示せず、ファイルに保存のみ
```

## ライセンス

このプロジェクトは教育目的で作成されています。

## 貢献

バグ報告や機能提案は、GitHubのIssuesでお願いします。

## 参考資料

- [py3dbp](https://github.com/enzoruiz/3dbinpacking) - 使用している3Dビンパッキングライブラリ
- [matplotlib](https://matplotlib.org/) - 可視化ライブラリ