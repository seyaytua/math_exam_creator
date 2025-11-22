# -*- coding: utf-8 -*-
"""外部スクリプト設定ダイアログ"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QGroupBox, QLabel,
    QFileDialog, QTextEdit, QMessageBox, QTabWidget,
    QWidget
)
from PySide6.QtCore import Qt


class ExternalScriptsDialog(QDialog):
    """外部スクリプト設定ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("外部スクリプト設定")
        self.setMinimumSize(700, 600)
        self.script_configs = []
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # 説明
        intro_label = QLabel(
            "外部のPythonスクリプトを登録して、アプリケーションから実行できます。\n"
            "最大3つのスクリプトを登録可能です。"
        )
        intro_label.setStyleSheet("""
            padding: 10px;
            background-color: #e3f2fd;
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        
        # 3つのスクリプト設定タブを作成
        for i in range(3):
            script_tab = self.create_script_tab(i + 1)
            self.script_configs.append(script_tab)
            self.tab_widget.addTab(script_tab['widget'], f"スクリプト {i + 1}")
        
        layout.addWidget(self.tab_widget)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        test_button = QPushButton("選択中のスクリプトをテスト実行")
        test_button.clicked.connect(self.test_current_script)
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(test_button)
        
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_and_close)
        save_button.setDefault(True)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def create_script_tab(self, number: int) -> dict:
        """スクリプト設定タブを作成
        
        Args:
            number: スクリプト番号（1-3）
        
        Returns:
            設定ウィジェットの辞書
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 基本情報グループ
        basic_group = QGroupBox("基本情報")
        basic_layout = QFormLayout()
        
        name_edit = QLineEdit()
        name_edit.setPlaceholderText(f"例: スクリプト{number}")
        basic_layout.addRow("スクリプト名:", name_edit)
        
        description_edit = QTextEdit()
        description_edit.setPlaceholderText("スクリプトの説明（オプション）")
        description_edit.setMaximumHeight(60)
        basic_layout.addRow("説明:", description_edit)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Python実行環境グループ
        python_group = QGroupBox("Python実行環境")
        python_layout = QVBoxLayout()
        
        python_path_layout = QHBoxLayout()
        python_path_edit = QLineEdit()
        python_path_edit.setPlaceholderText("Pythonインタープリタのパス")
        python_path_edit.setText(sys.executable)  # デフォルトは現在のPython
        python_path_layout.addWidget(python_path_edit)
        
        python_browse_button = QPushButton("参照...")
        python_browse_button.clicked.connect(
            lambda: self.browse_python(python_path_edit)
        )
        python_path_layout.addWidget(python_browse_button)
        
        python_layout.addLayout(python_path_layout)
        
        # Python検出ボタンとドロップダウン
        python_buttons_layout = QHBoxLayout()
        
        use_current_button = QPushButton("現在のPythonを使用")
        use_current_button.clicked.connect(
            lambda: python_path_edit.setText(sys.executable)
        )
        use_current_button.setStyleSheet("background-color: #e0e0e0;")
        python_buttons_layout.addWidget(use_current_button)
        
        detect_button = QPushButton("自動検出...")
        detect_button.clicked.connect(
            lambda: self.detect_python_installations(python_path_edit)
        )
        detect_button.setStyleSheet("background-color: #e0e0e0;")
        python_buttons_layout.addWidget(detect_button)
        
        python_layout.addLayout(python_buttons_layout)
        
        python_info_label = QLabel(f"現在のPython: {sys.executable}")
        python_info_label.setStyleSheet("color: #666; font-size: 9pt;")
        python_info_label.setWordWrap(True)
        python_layout.addWidget(python_info_label)
        
        python_group.setLayout(python_layout)
        layout.addWidget(python_group)
        
        # スクリプトファイルグループ
        script_group = QGroupBox("スクリプトファイル")
        script_layout = QVBoxLayout()
        
        script_path_layout = QHBoxLayout()
        script_path_edit = QLineEdit()
        script_path_edit.setPlaceholderText(".pyファイルを選択してください")
        script_path_layout.addWidget(script_path_edit)
        
        script_browse_button = QPushButton("参照...")
        script_browse_button.clicked.connect(
            lambda: self.browse_script(script_path_edit)
        )
        script_path_layout.addWidget(script_browse_button)
        
        script_layout.addLayout(script_path_layout)
        
        script_group.setLayout(script_layout)
        layout.addWidget(script_group)
        
        layout.addStretch()
        
        return {
            'widget': widget,
            'name_edit': name_edit,
            'description_edit': description_edit,
            'python_path_edit': python_path_edit,
            'script_path_edit': script_path_edit
        }
    
    def browse_python(self, line_edit: QLineEdit):
        """Pythonインタープリタを選択"""
        # Windows の場合は .exe を探す
        if sys.platform.startswith('win'):
            file_filter = "実行ファイル (python.exe python3.exe);;すべてのファイル (*)"
        else:
            file_filter = "すべてのファイル (*)"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pythonインタープリタを選択",
            str(Path.home()),
            file_filter
        )
        
        if file_path:
            line_edit.setText(file_path)
    
    def browse_script(self, line_edit: QLineEdit):
        """スクリプトファイルを選択"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pythonスクリプトを選択",
            str(Path.home()),
            "Pythonスクリプト (*.py);;すべてのファイル (*)"
        )
        
        if file_path:
            line_edit.setText(file_path)
    
    def detect_python_installations(self, line_edit: QLineEdit):
        """システム内のPythonインストールを検出して選択"""
        from ..utils import PythonDetector
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel
        
        # Pythonインストールを検索
        python_paths = PythonDetector.find_python_installations()
        
        if not python_paths:
            QMessageBox.information(
                self, "Pythonが見つかりません",
                "システム内にPythonインストールが見つかりませんでした。\n"
                "手動でパスを指定してください。"
            )
            return
        
        # 選択ダイアログを作成
        dialog = QDialog(self)
        dialog.setWindowTitle("Pythonインストールを選択")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        info_label = QLabel(f"検出されたPythonインストール: {len(python_paths)}個")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        list_widget = QListWidget()
        
        # バージョン情報を取得して表示
        for python_path in python_paths:
            version = PythonDetector.get_python_version(python_path)
            if version:
                display_text = f"{python_path}  (Python {version})"
            else:
                display_text = python_path
            list_widget.addItem(display_text)
        
        list_widget.setCurrentRow(0)
        layout.addWidget(list_widget)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        select_button = QPushButton("選択")
        select_button.setDefault(True)
        select_button.clicked.connect(dialog.accept)
        button_layout.addWidget(select_button)
        
        layout.addLayout(button_layout)
        
        if dialog.exec() == QDialog.Accepted:
            selected_index = list_widget.currentRow()
            if 0 <= selected_index < len(python_paths):
                selected_path = python_paths[selected_index]
                line_edit.setText(selected_path)
    
    def test_current_script(self):
        """選択中のスクリプトをテスト実行"""
        current_index = self.tab_widget.currentIndex()
        config = self.script_configs[current_index]
        
        script_name = config['name_edit'].text() or f"スクリプト{current_index + 1}"
        python_path = config['python_path_edit'].text()
        script_path = config['script_path_edit'].text()
        
        # バリデーション
        if not script_path:
            QMessageBox.warning(
                self, "エラー",
                "スクリプトファイルが選択されていません。"
            )
            return
        
        if not Path(script_path).exists():
            QMessageBox.warning(
                self, "エラー",
                f"スクリプトファイルが見つかりません:\n{script_path}"
            )
            return
        
        if not python_path or not Path(python_path).exists():
            QMessageBox.warning(
                self, "エラー",
                f"Pythonインタープリタが見つかりません:\n{python_path}"
            )
            return
        
        # 実行確認
        reply = QMessageBox.question(
            self, "テスト実行",
            f"スクリプト '{script_name}' をテスト実行しますか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.execute_script(script_name, python_path, script_path)
    
    def execute_script(self, name: str, python_path: str, script_path: str):
        """スクリプトを実行"""
        import subprocess
        import sys
        import os
        
        try:
            # プラットフォーム別の設定
            startupinfo = None
            creationflags = 0
            extra_kwargs = {}
            
            if sys.platform == 'win32':
                # Windows: コンソールウィンドウを非表示
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = subprocess.CREATE_NO_WINDOW
            elif sys.platform == 'darwin':
                # macOS: 新しいターミナルウィンドウを開かない
                extra_kwargs['start_new_session'] = True
            
            # 環境変数をコピー
            env = os.environ.copy()
            
            # スクリプトを実行（タイムアウトなし）
            result = subprocess.run(
                [python_path, script_path],
                capture_output=True,
                text=True,
                # timeout: なし - スクリプトが完了するまで待機
                cwd=Path(script_path).parent,  # スクリプトのディレクトリで実行
                startupinfo=startupinfo,
                creationflags=creationflags,
                env=env,
                stdin=subprocess.DEVNULL,  # 標準入力を無効化
                **extra_kwargs
            )
            
            # 結果を表示
            from .script_output_dialog import ScriptOutputDialog
            output_dialog = ScriptOutputDialog(
                name,
                result.stdout,
                result.stderr,
                result.returncode,
                self
            )
            output_dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(
                self, "実行エラー",
                f"スクリプトの実行中にエラーが発生しました:\n{str(e)}"
            )
    
    def load_settings(self):
        """設定を読み込み"""
        from ..config import config
        
        for i in range(3):
            script_config = config.get(f'external_scripts.script{i+1}', {})
            if script_config:
                self.script_configs[i]['name_edit'].setText(
                    script_config.get('name', '')
                )
                self.script_configs[i]['description_edit'].setPlainText(
                    script_config.get('description', '')
                )
                self.script_configs[i]['python_path_edit'].setText(
                    script_config.get('python_path', sys.executable)
                )
                self.script_configs[i]['script_path_edit'].setText(
                    script_config.get('script_path', '')
                )
    
    def save_and_close(self):
        """設定を保存して閉じる"""
        from ..config import config
        
        for i in range(3):
            script_config = {
                'name': self.script_configs[i]['name_edit'].text(),
                'description': self.script_configs[i]['description_edit'].toPlainText(),
                'python_path': self.script_configs[i]['python_path_edit'].text(),
                'script_path': self.script_configs[i]['script_path_edit'].text()
            }
            config.set(f'external_scripts.script{i+1}', script_config)
        
        QMessageBox.information(
            self, "保存完了",
            "外部スクリプトの設定を保存しました。"
        )
        self.accept()
    
    def get_all_scripts(self) -> list:
        """すべてのスクリプト設定を取得
        
        Returns:
            スクリプト設定のリスト
        """
        scripts = []
        for i, config in enumerate(self.script_configs):
            name = config['name_edit'].text()
            script_path = config['script_path_edit'].text()
            
            # 名前とパスが両方設定されている場合のみ追加
            if name and script_path:
                scripts.append({
                    'number': i + 1,
                    'name': name,
                    'description': config['description_edit'].toPlainText(),
                    'python_path': config['python_path_edit'].text(),
                    'script_path': script_path
                })
        
        return scripts
