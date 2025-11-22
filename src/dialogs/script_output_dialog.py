# -*- coding: utf-8 -*-
"""スクリプト実行結果表示ダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QGroupBox, QTabWidget,
    QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ScriptOutputDialog(QDialog):
    """スクリプト実行結果表示ダイアログ"""
    
    def __init__(self, script_name: str, stdout: str, stderr: str, 
                 return_code: int, parent=None):
        """
        Args:
            script_name: スクリプト名
            stdout: 標準出力
            stderr: 標準エラー出力
            return_code: 終了コード
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.script_name = script_name
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        self.setWindowTitle(f"スクリプト実行結果: {self.script_name}")
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(self)
        
        # ヘッダー情報
        header_layout = QHBoxLayout()
        
        name_label = QLabel(f"<b>スクリプト:</b> {self.script_name}")
        name_label.setStyleSheet("font-size: 11pt;")
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        
        # 終了コードの表示（色分け）
        if self.return_code == 0:
            status_text = "成功"
            status_color = "#4caf50"
        else:
            status_text = "エラー"
            status_color = "#f44336"
        
        status_label = QLabel(
            f"<b>終了コード:</b> <span style='color: {status_color};'>"
            f"{self.return_code} ({status_text})</span>"
        )
        status_label.setStyleSheet("font-size: 11pt;")
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        # タブウィジェット
        tab_widget = QTabWidget()
        
        # 標準出力タブ
        stdout_widget = self.create_output_tab(
            self.stdout if self.stdout else "(出力なし)",
            is_error=False
        )
        tab_widget.addTab(stdout_widget, "標準出力")
        
        # 標準エラー出力タブ
        stderr_widget = self.create_output_tab(
            self.stderr if self.stderr else "(エラー出力なし)",
            is_error=True
        )
        tab_widget.addTab(stderr_widget, "エラー出力")
        
        # 統合出力タブ
        combined_output = ""
        if self.stdout:
            combined_output += "=== 標準出力 ===\n" + self.stdout + "\n\n"
        if self.stderr:
            combined_output += "=== エラー出力 ===\n" + self.stderr
        if not combined_output:
            combined_output = "(出力なし)"
        
        combined_widget = self.create_output_tab(combined_output, is_error=False)
        tab_widget.addTab(combined_widget, "すべての出力")
        
        layout.addWidget(tab_widget)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("閉じる")
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        close_button.setStyleSheet("""
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
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # エラーがある場合は自動的にエラー出力タブを表示
        if self.return_code != 0 and self.stderr:
            tab_widget.setCurrentIndex(1)
    
    def create_output_tab(self, text: str, is_error: bool = False) -> QWidget:
        """出力表示タブを作成
        
        Args:
            text: 表示するテキスト
            is_error: エラー出力かどうか
        
        Returns:
            タブウィジェット
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # テキスト表示
        text_edit = QTextEdit()
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)
        
        # 等幅フォント
        font = QFont("Courier New", 9)
        font.setStyleHint(QFont.Monospace)
        text_edit.setFont(font)
        
        # エラー出力の場合は背景色を変更
        if is_error and text.strip() and text.strip() != "(エラー出力なし)":
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #fff3e0;
                    border: 1px solid #ff9800;
                }
            """)
        else:
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #f5f5f5;
                    border: 1px solid #ccc;
                }
            """)
        
        layout.addWidget(text_edit)
        
        return widget
