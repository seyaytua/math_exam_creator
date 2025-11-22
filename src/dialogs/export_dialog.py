# -*- coding: utf-8 -*-
"""エクスポートダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QCheckBox, QSpinBox, QPushButton,
    QGroupBox, QLabel, QComboBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt


class ExportDialog(QDialog):
    """エクスポート設定ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("エクスポート設定")
        self.setMinimumWidth(450)
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # 出力形式
        format_group = QGroupBox("出力形式")
        format_layout = QVBoxLayout()
        
        self.format_button_group = QButtonGroup()
        
        self.html_radio = QRadioButton("HTML（ブラウザで表示・印刷）")
        self.html_radio.setChecked(True)
        self.format_button_group.addButton(self.html_radio, 0)
        format_layout.addWidget(self.html_radio)
        
        self.pdf_radio = QRadioButton("PDF（直接印刷可能）")
        self.pdf_radio.setEnabled(True)
        self.format_button_group.addButton(self.pdf_radio, 1)
        format_layout.addWidget(self.pdf_radio)
        
        # PDF出力の利用可能性をチェック
        from ..exporters import PDFExporter
        pdf_exporter = PDFExporter()
        available, library = pdf_exporter.is_available()
        
        if not available:
            self.pdf_radio.setEnabled(False)
            pdf_note = QLabel("※ PDF出力には weasyprint または xhtml2pdf のインストールが必要です")
            pdf_note.setStyleSheet("color: #ff6600; font-size: 10pt; margin-left: 20px;")
            format_layout.addWidget(pdf_note)
        else:
            pdf_note = QLabel(f"※ PDF出力エンジン: {library}")
            pdf_note.setStyleSheet("color: #4caf50; font-size: 10pt; margin-left: 20px;")
            format_layout.addWidget(pdf_note)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # ページレイアウト設定
        page_group = QGroupBox("ページレイアウト")
        page_layout = QFormLayout()
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "B5", "Letter"])
        page_layout.addRow("用紙サイズ:", self.page_size_combo)
        
        self.problems_per_page_spin = QSpinBox()
        self.problems_per_page_spin.setRange(1, 2)
        self.problems_per_page_spin.setValue(1)
        self.problems_per_page_spin.setSuffix(" 問")
        page_layout.addRow("1ページあたりの大問数:", self.problems_per_page_spin)
        
        page_note = QLabel("※ 1問または2問を選択できます")
        page_note.setStyleSheet("color: #666; font-size: 10pt; margin-left: 10px;")
        page_layout.addRow("", page_note)
        
        page_group.setLayout(page_layout)
        layout.addWidget(page_group)
        
        # コンテンツ設定
        content_group = QGroupBox("表示内容")
        content_layout = QVBoxLayout()
        
        self.show_cover_check = QCheckBox("表紙を含める")
        self.show_cover_check.setChecked(True)
        content_layout.addWidget(self.show_cover_check)
        
        self.show_problem_numbers_check = QCheckBox("問題番号を表示")
        self.show_problem_numbers_check.setChecked(True)
        content_layout.addWidget(self.show_problem_numbers_check)
        
        self.show_answers_check = QCheckBox("解答を表示")
        self.show_answers_check.setChecked(False)
        self.show_answers_check.setEnabled(False)
        content_layout.addWidget(self.show_answers_check)
        
        answer_note = QLabel("※ 解答表示機能は今後実装予定です")
        answer_note.setStyleSheet("color: #999; font-size: 10pt; margin-left: 20px;")
        content_layout.addWidget(answer_note)
        
        self.generate_answer_sheet_check = QCheckBox("解答用紙を自動生成")
        self.generate_answer_sheet_check.setChecked(True)
        content_layout.addWidget(self.generate_answer_sheet_check)
        
        answer_sheet_note = QLabel("※ 問題文から空欄（ア、イ、ウ等）を抽出して解答用紙を生成します")
        answer_sheet_note.setStyleSheet("color: #666; font-size: 10pt; margin-left: 20px;")
        content_layout.addWidget(answer_sheet_note)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # スタイル設定
        style_group = QGroupBox("スタイル")
        style_layout = QFormLayout()
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        self.font_size_spin.setValue(12)
        self.font_size_spin.setSuffix(" pt")
        style_layout.addRow("フォントサイズ:", self.font_size_spin)
        
        self.line_spacing_combo = QComboBox()
        self.line_spacing_combo.addItems(["狭い (1.5)", "標準 (1.8)", "広い (2.0)"])
        self.line_spacing_combo.setCurrentIndex(1)
        style_layout.addRow("行間:", self.line_spacing_combo)
        
        self.margin_combo = QComboBox()
        self.margin_combo.addItems(["狭い (15mm)", "標準 (20mm)", "広い (25mm)"])
        self.margin_combo.setCurrentIndex(1)
        style_layout.addRow("余白:", self.margin_combo)
        
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        ok_button = QPushButton("エクスポート")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        ok_button.setStyleSheet("""
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
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
    
    def get_options(self):
        """設定値を取得"""
        line_spacing_map = {
            0: 1.5,
            1: 1.8,
            2: 2.0
        }
        line_spacing = line_spacing_map.get(self.line_spacing_combo.currentIndex(), 1.8)
        
        margin_map = {
            0: "15mm",
            1: "20mm",
            2: "25mm"
        }
        margin = margin_map.get(self.margin_combo.currentIndex(), "20mm")
        
        return {
            'format': 'html' if self.html_radio.isChecked() else 'pdf',
            'page_size': self.page_size_combo.currentText(),
            'problems_per_page': self.problems_per_page_spin.value(),
            'show_cover': self.show_cover_check.isChecked(),
            'show_problem_numbers': self.show_problem_numbers_check.isChecked(),
            'show_answers': self.show_answers_check.isChecked(),
            'generate_answer_sheet': self.generate_answer_sheet_check.isChecked(),
            'font_size': self.font_size_spin.value(),
            'line_spacing': line_spacing,
            'margin': margin
        }
