# -*- coding: utf-8 -*-
"""画像挿入ダイアログ"""

import base64
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox,
    QFormLayout, QFileDialog, QGroupBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ImageInsertDialog(QDialog):
    """画像挿入ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("画像を挿入")
        self.setMinimumWidth(500)
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # 画像選択グループ
        file_group = QGroupBox("画像ファイル")
        file_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("画像ファイルを選択してください")
        file_layout.addWidget(self.file_path_edit)
        
        browse_button = QPushButton("参照...")
        browse_button.clicked.connect(self.browse_image)
        file_layout.addWidget(browse_button)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # プレビュー
        preview_group = QGroupBox("プレビュー")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("画像が選択されていません")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                background-color: #f9f9f9;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # 画像設定グループ
        settings_group = QGroupBox("画像設定")
        settings_layout = QFormLayout()
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(50, 1000)
        self.width_spin.setValue(400)
        self.width_spin.setSuffix(" px")
        settings_layout.addRow("幅:", self.width_spin)
        
        self.alt_text_edit = QLineEdit()
        self.alt_text_edit.setPlaceholderText("例: グラフ、図形、写真")
        settings_layout.addRow("代替テキスト:", self.alt_text_edit)
        
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["左寄せ", "中央揃え", "右寄せ"])
        self.alignment_combo.setCurrentIndex(1)
        settings_layout.addRow("配置:", self.alignment_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        insert_button = QPushButton("挿入")
        insert_button.clicked.connect(self.accept)
        insert_button.setDefault(True)
        insert_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 6px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        button_layout.addWidget(insert_button)
        
        layout.addLayout(button_layout)
    
    def browse_image(self):
        """画像ファイルを選択"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "画像を選択",
            str(Path.home()),
            "画像ファイル (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;すべてのファイル (*)"
        )
        
        if file_path:
            self.selected_file = Path(file_path)
            self.file_path_edit.setText(str(self.selected_file))
            self.update_preview()
    
    def update_preview(self):
        """プレビューを更新"""
        if not self.selected_file or not self.selected_file.exists():
            return
        
        pixmap = QPixmap(str(self.selected_file))
        if not pixmap.isNull():
            # プレビューサイズに合わせて縮小
            scaled_pixmap = pixmap.scaled(
                400, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
        else:
            self.preview_label.setText("画像を読み込めませんでした")
    
    def get_image_html(self) -> str:
        """画像のHTMLコードを取得"""
        if not self.selected_file or not self.selected_file.exists():
            return ""
        
        # 画像をBase64エンコード
        with open(self.selected_file, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # MIMEタイプを取得
        suffix = self.selected_file.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.svg': 'image/svg+xml'
        }
        mime_type = mime_types.get(suffix, 'image/png')
        
        # 配置スタイルを取得
        alignment_styles = {
            0: 'text-align: left;',
            1: 'text-align: center;',
            2: 'text-align: right;'
        }
        alignment_style = alignment_styles.get(self.alignment_combo.currentIndex(), 'text-align: center;')
        
        width = self.width_spin.value()
        alt_text = self.alt_text_edit.text() or "画像"
        
        # HTMLコードを生成
        html = f'''<div style="{alignment_style}">
    <img src="data:{mime_type};base64,{base64_data}" alt="{alt_text}" width="{width}" style="max-width: 100%;" />
</div>'''
        
        return html
    
    def get_image_markdown(self) -> str:
        """画像のMarkdownコードを取得（Base64埋め込み）"""
        if not self.selected_file or not self.selected_file.exists():
            return ""
        
        # 画像をBase64エンコード
        with open(self.selected_file, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # MIMEタイプを取得
        suffix = self.selected_file.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.svg': 'image/svg+xml'
        }
        mime_type = mime_types.get(suffix, 'image/png')
        
        alt_text = self.alt_text_edit.text() or "画像"
        
        # Markdownコードを生成（HTML形式で埋め込み）
        width = self.width_spin.value()
        markdown = f'<img src="data:{mime_type};base64,{base64_data}" alt="{alt_text}" width="{width}" />'
        
        return markdown
