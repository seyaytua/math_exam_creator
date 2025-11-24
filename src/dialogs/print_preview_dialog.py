"""印刷プレビューダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QSpinBox, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl, Signal, QTimer, QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from typing import Dict, Optional


class PrintPreviewDialog(QDialog):
    """印刷プレビューダイアログ"""
    
    def __init__(self, html_content: str, settings: Dict, parent=None):
        super().__init__(parent)
        self.html_content = html_content
        self.settings = settings
        self.printer = QPrinter(QPrinter.HighResolution)
        
        self.setWindowTitle("印刷プレビュー")
        self.setMinimumSize(1000, 800)
        
        self._init_ui()
        self._apply_print_settings()
        self._load_content()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ツールバー
        toolbar_layout = QHBoxLayout()
        
        # ズームコントロール
        toolbar_layout.addWidget(QLabel("ズーム:"))
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["50%", "75%", "100%", "125%", "150%", "200%"])
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self._on_zoom_changed)
        toolbar_layout.addWidget(self.zoom_combo)
        
        toolbar_layout.addStretch()
        
        # 印刷設定情報
        settings_info = self._get_settings_info()
        info_label = QLabel(settings_info)
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        toolbar_layout.addWidget(info_label)
        
        toolbar_layout.addStretch()
        
        # 印刷ボタン
        print_btn = QPushButton("印刷...")
        print_btn.clicked.connect(self._print_document)
        toolbar_layout.addWidget(print_btn)
        
        # 閉じるボタン
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.close)
        toolbar_layout.addWidget(close_btn)
        
        layout.addLayout(toolbar_layout)
        
        # プレビューエリア (QWebEngineView)
        self.web_view = QWebEngineView()
        self.web_view.setZoomFactor(1.0)
        layout.addWidget(self.web_view)
    
    def _apply_print_settings(self):
        """印刷設定をプリンターに適用"""
        # 用紙サイズ
        paper_size_map = {
            'A4': QPageSize.PageSizeId.A4,
            'A3': QPageSize.PageSizeId.A3,
            'B4': QPageSize.PageSizeId.B4,
            'B5': QPageSize.PageSizeId.B5,
            'Letter': QPageSize.PageSizeId.Letter,
            'Legal': QPageSize.PageSizeId.Legal,
        }
        paper_size = self.settings.get('paper_size', 'A4')
        page_size_id = paper_size_map.get(paper_size, QPageSize.PageSizeId.A4)
        
        # 向き
        orientation = self.settings.get('orientation', 'portrait')
        qt_orientation = (QPageLayout.Orientation.Portrait 
                         if orientation == 'portrait' 
                         else QPageLayout.Orientation.Landscape)
        
        # マージン (mm)
        left = float(self.settings.get('margin_left', 20))
        top = float(self.settings.get('margin_top', 20))
        right = float(self.settings.get('margin_right', 20))
        bottom = float(self.settings.get('margin_bottom', 20))
        
        margins = QMarginsF(left, top, right, bottom)
        
        # QPageLayoutを作成（コンストラクタで一括設定）
        # 引数: PageSize, Orientation, Margins, Units(Millimeter)
        page_layout = QPageLayout(
            QPageSize(page_size_id),
            qt_orientation,
            margins,
            QPageLayout.Unit.Millimeter
        )
        
        self.printer.setPageLayout(page_layout)
    
    def _get_settings_info(self) -> str:
        """設定情報の文字列を取得"""
        paper_size = self.settings.get('paper_size', 'A4')
        orientation = "縦" if self.settings.get('orientation') == 'portrait' else "横"
        copies = self.settings.get('copies', 1)
        
        parts = [f"用紙: {paper_size} {orientation}"]
        
        if copies > 1:
            parts.append(f"部数: {copies}")
        
        options = []
        if self.settings.get('include_cover', True):
            options.append("表紙")
        if self.settings.get('include_problems', True):
            options.append("問題")
        if self.settings.get('include_answer_sheet', False):
            options.append("解答用紙")
        if self.settings.get('show_page_numbers', True):
            options.append("ページ番号")
        
        if options:
            parts.append(f"印刷項目: {', '.join(options)}")
        
        return " | ".join(parts)
    
    def _load_content(self):
        """HTMLコンテンツをロード"""
        self.web_view.setHtml(self.html_content)
    
    def _on_zoom_changed(self, text: str):
        """ズーム変更時の処理"""
        try:
            zoom_value = int(text.replace('%', ''))
            self.web_view.setZoomFactor(zoom_value / 100.0)
        except ValueError:
            pass
    
    def _print_document(self):
        """実際に印刷を実行"""
        # 印刷ダイアログを表示
        dialog = QPrintDialog(self.printer, self)
        dialog.setWindowTitle("印刷")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # QWebEngineViewから印刷
            # 印刷完了を待つためにコールバックを使用
            def print_finished(success):
                if success:
                    QMessageBox.information(
                        self,
                        "印刷",
                        "印刷を開始しました。"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "印刷エラー",
                        "印刷に失敗しました。"
                    )
            
            # QWebEngineViewのprintメソッドを使用
            self.web_view.page().print(self.printer, print_finished)
