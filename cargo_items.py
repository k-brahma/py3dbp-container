"""
貨物アイテム定義モジュール
========================

CSVファイルから貨物データを読み込む関数を提供します。

Functions:
----------
create_cargo_items
    色名の貨物アイテムを読み込む
create_test_cargo_items
    テスト用の貨物アイテムを読み込む
create_japanese_cargo_items
    日本語名の貨物アイテムを読み込む
"""

import pandas as pd
import os
from pathlib import Path


def _load_cargo_from_csv(filename):
    """
    CSVファイルから貨物データを読み込む共通関数。
    
    Parameters:
    -----------
    filename : str
        読み込むCSVファイル名
        
    Returns:
    --------
    list
        貨物アイテムの辞書のリスト
    """
    # ファイルパスを構築
    base_dir = Path(__file__).parent
    csv_path = base_dir / 'sample_data' / filename
    
    # CSVが存在しない場合はデフォルト値を返す
    if not csv_path.exists():
        print(f"警告: {csv_path} が見つかりません。デフォルト値を使用します。")
        return _get_default_items(filename)
    
    try:
        # CSVを読み込み
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        # 必要なカラムがあるかチェック（新旧両方の形式に対応）
        required_columns_m = ['名前', '幅(m)', '高さ(m)', '奥行き(m)', '重量(kg)', '個数']
        required_columns_mm = ['名前', '幅(mm)', '高さ(mm)', '奥行き(mm)', '重量(g)', '個数']
        
        if all(col in df.columns for col in required_columns_m):
            # メートル単位の場合
            items = []
            for _, row in df.iterrows():
                items.append({
                    'name': row['名前'],
                    'width': float(row['幅(m)']),
                    'height': float(row['高さ(m)']),
                    'depth': float(row['奥行き(m)']),
                    'weight': float(row['重量(kg)']),
                    'count': int(row['個数'])
                })
        elif all(col in df.columns for col in required_columns_mm):
            # ミリメートル単位の場合（メートルに変換）
            items = []
            for _, row in df.iterrows():
                items.append({
                    'name': row['名前'],
                    'width': float(row['幅(mm)']) / 1000.0,
                    'height': float(row['高さ(mm)']) / 1000.0,
                    'depth': float(row['奥行き(mm)']) / 1000.0,
                    'weight': float(row['重量(g)']) / 1000.0,
                    'count': int(row['個数'])
                })
        else:
            print(f"警告: {csv_path} のカラムが正しくありません。")
        
        return items
        
    except Exception as e:
        print(f"エラー: CSVファイルの読み込みに失敗しました: {e}")



def create_cargo_items():
    """
    貨物アイテムを定義する関数。
    sample_data/color_cargo_items.csv から読み込む。
    
    Returns:
    --------
    list
        色名の貨物アイテムのリスト
    """
    return _load_cargo_from_csv('color_cargo_items.csv')


def create_test_cargo_items():
    """
    テスト用の貨物アイテムを定義する関数。
    sample_data/test_cargo_items.csv から読み込む。
    
    Returns:
    --------
    list
        テスト用の貨物アイテムのリスト
    """
    return _load_cargo_from_csv('test_cargo_items.csv')


def create_japanese_cargo_items():
    """
    日本語名の貨物アイテムを定義する関数。
    sample_data/japanese_cargo_items.csv から読み込む。
    
    Returns:
    --------
    list
        日本語名の貨物アイテムのリスト
    """
    return _load_cargo_from_csv('japanese_cargo_items.csv')


# CSVファイルのテンプレートを生成する関数
def create_csv_template(output_path='sample_data/template_cargo_items.csv'):
    """
    貨物データのCSVテンプレートを生成する。
    
    Parameters:
    -----------
    output_path : str
        出力先のパス
    """
    template_data = {
        '名前': ['標準パレット', '大型ボックス', '機械部品'],
        '幅(m)': [1.2, 2.0, 1.5],
        '高さ(m)': [1.5, 1.8, 1.2],
        '奥行き(m)': [1.0, 1.5, 1.0],
        '重量(kg)': [800, 1500, 1000],
        '個数': [10, 5, 8]
    }
    
    df = pd.DataFrame(template_data)
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # CSVとして保存
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"テンプレートCSVを作成しました: {output_path}")