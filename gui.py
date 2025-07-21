"""
コンテナパッキングGUIアプリケーション
=====================================

Tkinterを使用したグラフィカルユーザーインターフェース。
貨物の登録、編集、削除、およびパッキング実行機能を提供します。

Classes:
--------
ContainerPackingGUI
    メインGUIアプリケーションクラス
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from main_class import ContainerPackingApp
from cargo_items import create_cargo_items, create_test_cargo_items, create_japanese_cargo_items


class ContainerPackingGUI:
    """
    コンテナパッキングのGUIアプリケーションクラス。
    
    Attributes:
    -----------
    root : tk.Tk
        メインウィンドウ
    cargo_df : pd.DataFrame
        貨物データを管理するDataFrame
    packing_app : ContainerPackingApp
        パッキングアプリケーションのインスタンス
    """
    
    def __init__(self, root):
        """
        GUIアプリケーションを初期化する。
        
        Parameters:
        -----------
        root : tk.Tk
            Tkinterのルートウィンドウ
        """
        self.root = root
        self.root.title("コンテナパッキング管理システム")
        self.root.geometry("1200x800")
        
        # パッキングアプリケーションのインスタンス
        self.packing_app = ContainerPackingApp()
        
        # 貨物データを管理するDataFrame
        self.cargo_df = pd.DataFrame(columns=['名前', '幅(m)', '高さ(m)', '奥行き(m)', '重量(kg)', '個数'])
        
        # スタイル設定
        self.setup_styles()
        
        # GUI要素の作成
        self.create_widgets()
        
        # デフォルトの貨物を読み込む
        self.load_default_items()
        
    def setup_styles(self):
        """
        TTKスタイルを設定する。
        """
        style = ttk.Style()
        style.theme_use('clam')
        
        # カスタムスタイル
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
    def create_widgets(self):
        """
        すべてのGUIウィジェットを作成する。
        """
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ウィンドウのグリッド設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 左側: 入力フォームエリア
        self.create_input_area(main_frame)
        
        # 右側: 貨物リスト表示エリア
        self.create_cargo_list_area(main_frame)
        
        # 下部: コンテナ設定とアクションボタン
        self.create_bottom_area(main_frame)
        
    def create_input_area(self, parent):
        """
        貨物入力フォームエリアを作成する。
        
        Parameters:
        -----------
        parent : ttk.Frame
            親フレーム
        """
        # 入力エリアフレーム
        input_frame = ttk.LabelFrame(parent, text="貨物登録", padding="10")
        input_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 入力フィールド
        fields = [
            ("貨物名:", "name"),
            ("幅 (m):", "width"),
            ("高さ (m):", "height"),
            ("奥行き (m):", "depth"),
            ("重量 (kg):", "weight"),
            ("個数:", "count")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
            self.entries[key] = entry
            
        # デフォルト値設定
        self.entries['count'].insert(0, "1")
        
        # ボタン
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="追加", command=self.add_cargo).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="クリア", command=self.clear_entries).grid(row=0, column=1, padx=5)
        
        # プリセットボタン
        preset_frame = ttk.LabelFrame(input_frame, text="プリセット", padding="5")
        preset_frame.grid(row=len(fields)+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(preset_frame, text="小型パレット", 
                  command=lambda: self.load_preset("小型パレット", 1.0, 1.0, 0.8, 400)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="標準パレット", 
                  command=lambda: self.load_preset("標準パレット", 1.2, 1.5, 1.0, 800)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="大型機械", 
                  command=lambda: self.load_preset("大型機械", 2.0, 2.0, 1.5, 2000)).pack(side=tk.LEFT, padx=2)
        
        # 一括読み込みボタン
        batch_frame = ttk.LabelFrame(input_frame, text="一括読み込み", padding="5")
        batch_frame.grid(row=len(fields)+2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(batch_frame, text="日本語セット", 
                  command=lambda: self.load_cargo_set('japanese')).pack(side=tk.LEFT, padx=2)
        ttk.Button(batch_frame, text="テストセット", 
                  command=lambda: self.load_cargo_set('test')).pack(side=tk.LEFT, padx=2)
        ttk.Button(batch_frame, text="色名セット", 
                  command=lambda: self.load_cargo_set('default')).pack(side=tk.LEFT, padx=2)
        
    def create_cargo_list_area(self, parent):
        """
        貨物リスト表示エリアを作成する。
        
        Parameters:
        -----------
        parent : ttk.Frame
            親フレーム
        """
        # リストエリアフレーム
        list_frame = ttk.LabelFrame(parent, text="貨物リスト", padding="10")
        list_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeviewウィジェット
        columns = ['名前', '幅(m)', '高さ(m)', '奥行き(m)', '重量(kg)', '個数']
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # カラムの設定
        for col in columns:
            self.tree.heading(col, text=col)
            if col == '名前':
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=80)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 配置
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # リストフレームのグリッド設定
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # リスト操作ボタン
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(list_button_frame, text="選択を削除", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_button_frame, text="すべてクリア", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_button_frame, text="CSVエクスポート", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_button_frame, text="CSVインポート", command=self.import_csv).pack(side=tk.LEFT, padx=5)
        
        # 統計情報
        self.stats_label = ttk.Label(list_frame, text="合計: 0個のアイテム")
        self.stats_label.grid(row=2, column=0, columnspan=2, pady=5)
        
    def create_bottom_area(self, parent):
        """
        コンテナ設定とアクションボタンエリアを作成する。
        
        Parameters:
        -----------
        parent : ttk.Frame
            親フレーム
        """
        # コンテナ設定フレーム
        container_frame = ttk.LabelFrame(parent, text="コンテナ設定", padding="10")
        container_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # コンテナ設定フィールド
        container_fields = [
            ("幅 (m):", "container_width", "12.03"),
            ("高さ (m):", "container_height", "2.39"),
            ("奥行き (m):", "container_depth", "2.35"),
            ("最大重量 (kg):", "container_max_weight", "28000")
        ]
        
        self.container_entries = {}
        for i, (label, key, default) in enumerate(container_fields):
            ttk.Label(container_frame, text=label).grid(row=0, column=i*2, sticky=tk.W, padx=(10, 5))
            entry = ttk.Entry(container_frame, width=10)
            entry.insert(0, default)
            entry.grid(row=0, column=i*2+1, sticky=(tk.W, tk.E), padx=(0, 10))
            self.container_entries[key] = entry
        
        # アクションボタンフレーム
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 実行ボタン
        self.pack_button = ttk.Button(action_frame, text="パッキング実行", 
                                     command=self.execute_packing, style='Accent.TButton')
        self.pack_button.pack(side=tk.LEFT, padx=10)
        
        # 結果表示ボタン
        self.view_button = ttk.Button(action_frame, text="結果を表示", 
                                     command=self.view_results, state='disabled')
        self.view_button.pack(side=tk.LEFT, padx=10)
        
        # パッキング結果表示エリア
        result_frame = ttk.LabelFrame(parent, text="パッキング結果", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 結果ラベル
        self.result_label = ttk.Label(result_frame, text="パッキングを実行してください", 
                                     font=('Arial', 10))
        self.result_label.pack(anchor=tk.W)
        
        # 積みきれなかったアイテムの表示エリア
        self.unfitted_frame = ttk.Frame(result_frame)
        self.unfitted_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 詳細表示ボタン（初期は非表示）
        self.details_button = ttk.Button(result_frame, text="積みきれなかったアイテムの詳細", 
                                       command=self.show_unfitted_details, state='disabled')
        self.details_button.pack(pady=(10, 0))
        self.details_button.pack_forget()  # 初期は非表示
            
    def add_cargo(self):
        """
        入力フォームから貨物を追加する。
        """
        try:
            # 入力値の取得と検証
            name = self.entries['name'].get().strip()
            if not name:
                messagebox.showerror("エラー", "貨物名を入力してください。")
                return
            
            # 数値フィールドの検証
            width = float(self.entries['width'].get())
            height = float(self.entries['height'].get())
            depth = float(self.entries['depth'].get())
            weight = float(self.entries['weight'].get())
            count = int(self.entries['count'].get())
            
            if any(val <= 0 for val in [width, height, depth, weight, count]):
                messagebox.showerror("エラー", "すべての数値は正の値である必要があります。")
                return
            
            # DataFrameに追加
            new_cargo = pd.DataFrame({
                '名前': [name],
                '幅(m)': [width],
                '高さ(m)': [height],
                '奥行き(m)': [depth],
                '重量(kg)': [weight],
                '個数': [count]
            })
            
            self.cargo_df = pd.concat([self.cargo_df, new_cargo], ignore_index=True)
            
            # Treeviewに追加
            self.tree.insert('', 'end', values=(name, width, height, depth, weight, count))
            
            # 統計情報更新
            self.update_stats()
            
            # エントリをクリア
            self.clear_entries()
            
        except ValueError:
            messagebox.showerror("エラー", "数値フィールドに有効な数値を入力してください。")
            
    def clear_entries(self):
        """
        入力フィールドをクリアする。
        """
        for key, entry in self.entries.items():
            if key == 'count':
                entry.delete(0, tk.END)
                entry.insert(0, "1")
            else:
                entry.delete(0, tk.END)
                
    def load_preset(self, name, width, height, depth, weight):
        """
        プリセット値を入力フィールドに設定する。
        
        Parameters:
        -----------
        name : str
            貨物名
        width : float
            幅
        height : float
            高さ
        depth : float
            奥行き
        weight : float
            重量
        """
        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, name)
        self.entries['width'].delete(0, tk.END)
        self.entries['width'].insert(0, str(width))
        self.entries['height'].delete(0, tk.END)
        self.entries['height'].insert(0, str(height))
        self.entries['depth'].delete(0, tk.END)
        self.entries['depth'].insert(0, str(depth))
        self.entries['weight'].delete(0, tk.END)
        self.entries['weight'].insert(0, str(weight))
        
    def delete_selected(self):
        """
        選択された貨物を削除する。
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "削除する項目を選択してください。")
            return
        
        # 確認ダイアログ
        if messagebox.askyesno("確認", f"{len(selected_items)}個の項目を削除しますか？"):
            # インデックスを取得して削除
            indices_to_delete = []
            for item in selected_items:
                index = self.tree.index(item)
                indices_to_delete.append(index)
                self.tree.delete(item)
            
            # DataFrameから削除
            self.cargo_df = self.cargo_df.drop(indices_to_delete).reset_index(drop=True)
            
            # 統計情報更新
            self.update_stats()
            
    def clear_all(self):
        """
        すべての貨物をクリアする。
        """
        if self.cargo_df.empty:
            return
            
        if messagebox.askyesno("確認", "すべての貨物をクリアしますか？"):
            # Treeviewをクリア
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # DataFrameをクリア
            self.cargo_df = pd.DataFrame(columns=['名前', '幅(mm)', '高さ(mm)', '奥行き(mm)', '重量(g)', '個数'])
            
            # 統計情報更新
            self.update_stats()
            
    def export_csv(self):
        """
        貨物リストをCSVファイルにエクスポートする。
        """
        if self.cargo_df.empty:
            messagebox.showwarning("警告", "エクスポートする貨物がありません。")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")],
            initialfile=f"cargo_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            initialdir="sample_data"
        )
        
        if filename:
            try:
                self.cargo_df.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("成功", f"貨物リストを{filename}に保存しました。")
            except Exception as e:
                messagebox.showerror("エラー", f"エクスポート中にエラーが発生しました: {str(e)}")
                
    def import_csv(self):
        """
        CSVファイルから貨物リストをインポートする。
        """
        filename = filedialog.askopenfilename(
            filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")],
            initialdir="sample_data"
        )
        
        if filename:
            try:
                # CSVを読み込み
                imported_df = pd.read_csv(filename, encoding='utf-8-sig')
                
                # カラムの検証（新旧両方の形式に対応）
                required_columns_m = ['名前', '幅(m)', '高さ(m)', '奥行き(m)', '重量(kg)', '個数']
                required_columns_mm = ['名前', '幅(mm)', '高さ(mm)', '奥行き(mm)', '重量(g)', '個数']
                
                if all(col in imported_df.columns for col in required_columns_m):
                    # メートル单位の場合はそのまま使用
                    pass
                elif all(col in imported_df.columns for col in required_columns_mm):
                    # ミリメートル单位の場合はメートルに変換
                    imported_df = imported_df.rename(columns={
                        '幅(mm)': '幅(m)', '高さ(mm)': '高さ(m)', 
                        '奥行き(mm)': '奥行き(m)', '重量(g)': '重量(kg)'
                    })
                    imported_df['幅(m)'] = imported_df['幅(m)'] / 1000.0
                    imported_df['高さ(m)'] = imported_df['高さ(m)'] / 1000.0
                    imported_df['奥行き(m)'] = imported_df['奥行き(m)'] / 1000.0
                    imported_df['重量(kg)'] = imported_df['重量(kg)'] / 1000.0
                else:
                    messagebox.showerror("エラー", "CSVファイルの形式が正しくありません。")
                    return
                
                # 既存のデータをクリア
                self.clear_all()
                
                # データを追加
                self.cargo_df = imported_df[required_columns_m].copy()
                
                # Treeviewに追加
                for _, row in self.cargo_df.iterrows():
                    self.tree.insert('', 'end', values=tuple(row))
                
                # 統計情報更新
                self.update_stats()
                
                messagebox.showinfo("成功", f"{len(self.cargo_df)}個の貨物をインポートしました。")
                
            except Exception as e:
                messagebox.showerror("エラー", f"インポート中にエラーが発生しました: {str(e)}")
                
    def update_stats(self):
        """
        統計情報を更新する。
        """
        total_items = self.cargo_df['個数'].sum() if not self.cargo_df.empty else 0
        unique_types = len(self.cargo_df) if not self.cargo_df.empty else 0
        self.stats_label.config(text=f"合計: {unique_types}種類, {total_items}個のアイテム")
        
    def load_default_items(self):
        """
        デフォルトの貨物アイテムを読み込む。
        """
        # 日本語セットをデフォルトで読み込む（確認なし）
        items = create_japanese_cargo_items()
        
        # DataFrameに追加
        for item in items:
            new_cargo = pd.DataFrame({
                '名前': [item['name']],
                '幅(m)': [item['width']],
                '高さ(m)': [item['height']],
                '奥行き(m)': [item['depth']],
                '重量(kg)': [item['weight']],
                '個数': [item['count']]
            })
            self.cargo_df = pd.concat([self.cargo_df, new_cargo], ignore_index=True)
            
            # Treeviewに追加
            self.tree.insert('', 'end', values=(
                item['name'], item['width'], item['height'], 
                item['depth'], item['weight'], item['count']
            ))
        
        # 統計情報更新
        self.update_stats()
        
    def load_cargo_set(self, set_name):
        """
        指定されたセットの貨物を一括で読み込む。
        
        Parameters:
        -----------
        set_name : str
            読み込むセット名 ('japanese', 'test', 'default')
        """
        # 既存のリストをクリア
        if not self.cargo_df.empty:
            if messagebox.askyesno("確認", "既存の貨物リストをクリアして新しいセットを読み込みますか？"):
                self.clear_all()
            else:
                return
        
        # セットを選択
        if set_name == 'japanese':
            items = create_japanese_cargo_items()
        elif set_name == 'test':
            items = create_test_cargo_items()
        else:
            items = create_cargo_items()
        
        # DataFrameに追加
        for item in items:
            new_cargo = pd.DataFrame({
                '名前': [item['name']],
                '幅(m)': [item['width']],
                '高さ(m)': [item['height']],
                '奥行き(m)': [item['depth']],
                '重量(kg)': [item['weight']],
                '個数': [item['count']]
            })
            self.cargo_df = pd.concat([self.cargo_df, new_cargo], ignore_index=True)
            
            # Treeviewに追加
            self.tree.insert('', 'end', values=(
                item['name'], item['width'], item['height'], 
                item['depth'], item['weight'], item['count']
            ))
        
        # 統計情報更新
        self.update_stats()
        
        messagebox.showinfo("読み込み完了", f"{set_name}セットを読み込みました。")
        
    def execute_packing(self):
        """
        パッキングを実行する。
        """
        if self.cargo_df.empty:
            messagebox.showwarning("警告", "パッキングする貨物がありません。")
            return
            
        try:
            # コンテナ設定を取得
            container_dims = {
                'width': float(self.container_entries['container_width'].get()),
                'height': float(self.container_entries['container_height'].get()),
                'depth': float(self.container_entries['container_depth'].get()),
                'max_weight': float(self.container_entries['container_max_weight'].get())
            }
            
            # 貨物データを適切な形式に変換
            items = []
            for _, row in self.cargo_df.iterrows():
                items.append({
                    'name': row['名前'],
                    'width': row['幅(m)'],
                    'height': row['高さ(m)'],
                    'depth': row['奥行き(m)'],
                    'weight': row['重量(kg)'],
                    'count': int(row['個数'])
                })
            
            # パッキング実行
            self.packing_app.setup_container(**container_dims)
            self.packing_app.pack_items(items)
            
            # 結果を取得
            efficiency = self.packing_app.print_results()
            
            # 結果の表示
            packed_count = len(self.packing_app.packing_engine.packed_items)
            unpacked_count = len(self.packing_app.packing_engine.unfitted_items)
            
            # 結果ラベルを更新
            result_text = f"積載効率: {efficiency:.1f}%  |  "
            result_text += f"配置済み: {packed_count}個  |  "
            result_text += f"配置不可: {unpacked_count}個"
            
            if unpacked_count == 0:
                result_text += "  ✓ すべて積載完了！"
                self.result_label.config(text=result_text, foreground='green')
            else:
                result_text += "  ⚠ 積みきれないアイテムがあります"
                self.result_label.config(text=result_text, foreground='red')
            
            # 既存の積みきれなかったアイテムの表示をクリア
            for widget in self.unfitted_frame.winfo_children():
                widget.destroy()
            
            # 積みきれなかったアイテムの詳細を表示
            if unpacked_count > 0:
                self.unfitted_stats = self.packing_app.packing_engine.get_unfitted_stats()
                
                # ヘッダー
                header_label = ttk.Label(self.unfitted_frame, text="積みきれなかったアイテム:", 
                                       font=('Arial', 10, 'bold'))
                header_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
                
                # アイテムリスト
                row = 1
                for item_name, count in self.unfitted_stats.items():
                    # アイテム名
                    ttk.Label(self.unfitted_frame, text=f"• {item_name}:").grid(
                        row=row, column=0, sticky=tk.W, padx=(20, 10))
                    # 個数
                    ttk.Label(self.unfitted_frame, text=f"{count}個", 
                            font=('Arial', 10, 'bold')).grid(
                        row=row, column=1, sticky=tk.W, padx=(0, 20))
                    # サイズ情報を安全に取得
                    try:
                        item_df = self.cargo_df[self.cargo_df['名前'] == item_name]
                        if not item_df.empty:
                            item_data = item_df.iloc[0]
                            size_text = f"({item_data['幅(m)']:.2f}×{item_data['高さ(m)']:.2f}×{item_data['奥行き(m)']:.2f}m)"
                        else:
                            size_text = "(サイズ情報なし)"
                    except Exception:
                        size_text = "(サイズ情報取得エラー)"
                    
                    ttk.Label(self.unfitted_frame, text=size_text, 
                            foreground='gray').grid(row=row, column=2, sticky=tk.W)
                    row += 1
                
                # 詳細ボタンを表示
                self.details_button.pack()
                self.details_button.config(state='normal')
            else:
                # 詳細ボタンを非表示
                self.details_button.pack_forget()
                self.details_button.config(state='disabled')
            
            # 結果表示ボタンを有効化
            self.view_button.config(state='normal')
            
        except ValueError as e:
            import traceback
            print("ValueError occurred:")
            traceback.print_exc()
            messagebox.showerror("エラー", "コンテナ設定に有効な数値を入力してください。")
            raise
        except Exception as e:
            import traceback
            print(f"Unexpected error occurred: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("エラー", f"パッキング中にエラーが発生しました: {str(e)}")
            raise
            
    def view_results(self):
        """
        パッキング結果を表示する。
        """
        if not hasattr(self.packing_app, 'packing_engine') or not self.packing_app.packing_engine:
            messagebox.showwarning("警告", "表示する結果がありません。")
            return
            
        # 新しいウィンドウで結果を表示
        result_window = tk.Toplevel(self.root)
        result_window.title("パッキング結果")
        result_window.geometry("800x600")
        
        # Figure作成
        fig, ax = self.packing_app.visualize_results()
        
        # Tkinterに埋め込み
        canvas = FigureCanvasTkAgg(fig, master=result_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 保存ボタン
        save_frame = ttk.Frame(result_window)
        save_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(save_frame, text="画像を保存", 
                  command=lambda: self.save_visualization(fig)).pack(side=tk.RIGHT)
        
    def save_visualization(self, fig):
        """
        可視化結果を保存する。
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            保存する図
        """
        efficiency = self.packing_app.packing_engine.get_load_efficiency(self.packing_app.container)
        title = (f'Container Packing: {self.packing_app.container.width} x '
                f'{self.packing_app.container.height} x {self.packing_app.container.depth}\n'
                f'Load Efficiency: {efficiency:.1f}%')
        
        filename = self.packing_app.save_visualization(fig, title)
        messagebox.showinfo("保存完了", f"画像を保存しました:\n{filename}")
    
    def show_unfitted_details(self):
        """
        積みきれなかったアイテムの詳細を表示する。
        """
        if hasattr(self, 'unfitted_stats'):
            self.show_unfitted_details_window(self.unfitted_stats)
    
    def show_unfitted_details_window(self, unfitted_stats):
        """
        積みきれなかったアイテムの詳細を別ウィンドウで表示する。
        
        Parameters:
        -----------
        unfitted_stats : dict
            アイテム名と個数の辞書
        """
        # 詳細ウィンドウを作成
        details_window = tk.Toplevel(self.root)
        details_window.title("積みきれなかったアイテムの詳細")
        details_window.geometry("600x400")
        
        # メインフレーム
        main_frame = ttk.Frame(details_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ラベル
        ttk.Label(main_frame, text="積みきれなかったアイテム一覧", 
                 style='Header.TLabel').pack(pady=(0, 10))
        
        # Treeviewで詳細表示
        columns = ['アイテム名', '個数', 'サイズ(m)', '重量(kg)']
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # 現在の貨物データから詳細情報を取得
        for item_name, count in unfitted_stats.items():
            try:
                # cargo_dfから該当アイテムの情報を取得
                item_df = self.cargo_df[self.cargo_df['名前'] == item_name]
                if not item_df.empty:
                    item_data = item_df.iloc[0]
                    size_str = f"{item_data['幅(m)']:.2f}×{item_data['高さ(m)']:.2f}×{item_data['奥行き(m)']:.2f}"
                    weight = item_data['重量(kg)']
                else:
                    size_str = "不明"
                    weight = "不明"
            except Exception as e:
                print(f"Error getting item data for {item_name}: {e}")
                size_str = "エラー"
                weight = "エラー"
            
            tree.insert('', 'end', values=(item_name, count, size_str, weight))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 提案メッセージ
        suggestion_frame = ttk.LabelFrame(main_frame, text="改善提案", padding="10")
        suggestion_frame.pack(fill=tk.X, pady=(10, 0))
        
        suggestion_text = "以下の対策を検討してください：\n"
        suggestion_text += "• 貨物サイズをさらに小さくする（現在70%）\n"
        suggestion_text += "• 大型アイテムの個数を減らす\n"
        suggestion_text += "• より大きなコンテナを使用する\n"
        suggestion_text += "• 複数のコンテナに分割する"
        
        ttk.Label(suggestion_frame, text=suggestion_text, wraplength=550).pack()
        
        # 閉じるボタン
        ttk.Button(main_frame, text="閉じる", 
                  command=details_window.destroy).pack(pady=(10, 0))


def main():
    """
    GUIアプリケーションを起動する。
    """
    root = tk.Tk()
    app = ContainerPackingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()