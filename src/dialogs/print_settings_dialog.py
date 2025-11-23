# -*- coding: utf-8 -*-
"""印刷設定ダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QGroupBox, QComboBox,
    QCheckBox, QSpinBox, QDoubleSpinBox, QRadioButton,
    QButtonGroup, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPageSetupDialog


class PrintSettingsDialog(QDialog):
    """印刷設定ダイアログ"""
    
    print_requested = Signal(dict)  # 印刷設定を返すシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.printer = QPrinter(QPrinter.HighResolution)
        self.setWindowTitle("印刷設定")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # 用紙設定グループ
        paper_group = QGroupBox("用紙設定")
        paper_layout = QFormLayout()
        
        self.paper_size_combo = QComboBox()
        self.paper_size_combo.addItems([
            "A4 (210 x 297 mm)",
            "A3 (297 x 420 mm)",
            "B4 (257 x 364 mm)",
            "B5 (182 x 257 mm)",
            "Letter (8.5 x 11 in)",
            "Legal (8.5 x 14 in)"
        ])
        paper_layout.addRow("用紙サイズ:", self.paper_size_combo)
        
        # 向き
        orientation_layout = QHBoxLayout()
        self.portrait_radio = QRadioButton("縦")
        self.portrait_radio.setChecked(True)
        self.landscape_radio = QRadioButton("横")
        
        self.orientation_group = QButtonGroup()
        self.orientation_group.addButton(self.portrait_radio, 0)
        self.orientation_group.addButton(self.landscape_radio, 1)
        
        orientation_layout.addWidget(self.portrait_radio)
        orientation_layout.addWidget(self.landscape_radio)
        orientation_layout.addStretch()
        paper_layout.addRow("向き:", orientation_layout)
        
        paper_group.setLayout(paper_layout)
        layout.addWidget(paper_group)
        
        # 余白設定グループ
        margin_group = QGroupBox("余白設定 (mm)")
        margin_layout = QFormLayout()
        
        self.top_margin_spin = QDoubleSpinBox()
        self.top_margin_spin.setRange(0, 100)
        self.top_margin_spin.setValue(15)
        self.top_margin_spin.setSuffix(" mm")
        margin_layout.addRow("上:", self.top_margin_spin)
        
        self.bottom_margin_spin = QDoubleSpinBox()
        self.bottom_margin_spin.setRange(0, 100)
        self.bottom_margin_spin.setValue(15)
        self.bottom_margin_spin.setSuffix(" mm")
        margin_layout.addRow("下:", self.bottom_margin_spin)
        
        self.left_margin_spin = QDoubleSpinBox()
        self.left_margin_spin.setRange(0, 100)
        self.left_margin_spin.setValue(20)
        self.left_margin_spin.setSuffix(" mm")
        margin_layout.addRow("左:", self.left_margin_spin)
        
        self.right_margin_spin = QDoubleSpinBox()
        self.right_margin_spin.setRange(0, 100)
        self.right_margin_spin.setValue(20)
        self.right_margin_spin.setSuffix(" mm")
        margin_layout.addRow("右:", self.right_margin_spin)
        
        margin_group.setLayout(margin_layout)
        layout.addWidget(margin_group)
        
        # 印刷オプショングループ
        options_group = QGroupBox("印刷オプション")
        options_layout = QVBoxLayout()
        
        self.print_cover_check = QCheckBox("表紙を印刷")
        self.print_cover_check.setChecked(True)
        options_layout.addWidget(self.print_cover_check)
        
        self.print_problems_check = QCheckBox("問題を印刷")
        self.print_problems_check.setChecked(True)
        options_layout.addWidget(self.print_problems_check)
        
        self.print_answer_sheet_check = QCheckBox("解答用紙を印刷")
        self.print_answer_sheet_check.setChecked(False)
        options_layout.addWidget(self.print_answer_sheet_check)
        
        self.page_numbers_check = QCheckBox("ページ番号を印刷")
        self.page_numbers_check.setChecked(True)
        options_layout.addWidget(self.page_numbers_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # コピー部数
        copies_layout = QHBoxLayout()
        copies_label = QLabel("印刷部数:")
        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 100)
        self.copies_spin.setValue(1)
        copies_layout.addWidget(copies_label)
        copies_layout.addWidget(self.copies_spin)
        copies_layout.addStretch()
        layout.addLayout(copies_layout)
        
        layout.addStretch()
        
        # ボタン
        button_layout = QHBoxLayout()
        
        self.page_setup_button = QPushButton("ページ設定...")
        self.page_setup_button.clicked.connect(self.open_page_setup)
        button_layout.addWidget(self.page_setup_button)
        
        button_layout.addStretch()
        
        self.preview_button = QPushButton("プレビュー")
        self.preview_button.clicked.connect(self.preview_print)
        button_layout.addWidget(self.preview_button)
        
        self.print_button = QPushButton("印刷")
        self.print_button.clicked.connect(self.print_document)
        self.print_button.setDefault(True)
        button_layout.addWidget(self.print_button)
        
        self.cancel_button = QPushButton("キャンセル")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_settings(self) -> dict:
        """現在の設定を取得"""
        return {
            'paper_size': self.paper_size_combo.currentText(),
            'orientation': 'portrait' if self.portrait_radio.isChecked() else 'landscape',
            'margin_top': self.top_margin_spin.value(),
            'margin_bottom': self.bottom_margin_spin.value(),
            'margin_left': self.left_margin_spin.value(),
            'margin_right': self.right_margin_spin.value(),
            'print_cover': self.print_cover_check.isChecked(),
            'print_problems': self.print_problems_check.isChecked(),
            'print_answer_sheet': self.print_answer_sheet_check.isChecked(),
            'page_numbers': self.page_numbers_check.isChecked(),
            'copies': self.copies_spin.value()
        }
    
    def open_page_setup(self):
        """ページ設定ダイアログを開く"""
        dialog = QPageSetupDialog(self.printer, self)
        if dialog.exec() == QDialog.Accepted:
            # プリンター設定を更新
            self._update_from_printer()
    
    def _update_from_printer(self):
        """プリンター設定からUIを更新"""
        # QPrinterの設定を読み取ってUIに反映
        if self.printer.pageLayout().orientation() == 0:  # Portrait
            self.portrait_radio.setChecked(True)
        else:
            self.landscape_radio.setChecked(True)
    
    def preview_print(self):
        """印刷プレビュー"""
        settings = self.get_settings()
        settings['action'] = 'preview'
        self.print_requested.emit(settings)
        self.accept()
    
    def print_document(self):
        """印刷ダイアログを表示"""
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec() == QDialog.Accepted:
            settings = self.get_settings()
            settings['action'] = 'print'
            settings['printer'] = self.printer
            self.print_requested.emit(settings)
            self.accept()
