# -*- coding: utf-8 -*-
"""HTML編集ウィジェット"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QLabel, QPushButton, QToolBar
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QTextOption, QAction
from PySide6.QtWebEngineWidgets import QWebEngineView


class HTMLEditor(QWidget):
    """HTML編集ウィジェット"""
    
    text_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._do_update_preview)
        self.scroll_position = 0
        self.init_ui()
        self._set_initial_html()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.create_toolbar(layout)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.editor = self.create_editor()
        splitter.addWidget(self.editor)
        
        self.preview = self.create_preview()
        splitter.addWidget(self.preview)
        
        splitter.setSizes([300, 900])
        
        layout.addWidget(splitter)
    
    def create_toolbar(self, parent_layout):
        """ツールバーを作成"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border-bottom: 1px solid #e0e0e0;
                padding: 4px;
                spacing: 2px;
            }
            QToolBar QToolButton {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 3px;
                padding: 4px 8px;
                margin: 2px;
            }
            QToolBar QToolButton:hover {
                background-color: #e3f2fd;
                border-color: #2196f3;
            }
        """)
        
        p_action = QAction("段落 <p>", self)
        p_action.triggered.connect(lambda: self.insert_html("<p>", "</p>"))
        toolbar.addAction(p_action)
        
        toolbar.addSeparator()
        
        inline_math_action = QAction("インライン数式", self)
        inline_math_action.triggered.connect(lambda: self.insert_html("$", "$"))
        toolbar.addAction(inline_math_action)
        
        display_math_action = QAction("ディスプレイ数式", self)
        display_math_action.triggered.connect(lambda: self.insert_html("\n$$\n", "\n$$\n"))
        toolbar.addAction(display_math_action)
        
        toolbar.addSeparator()
        
        table_action = QAction("表を挿入", self)
        table_action.triggered.connect(self.insert_table)
        toolbar.addAction(table_action)
        
        parent_layout.addWidget(toolbar)
    
    def create_editor(self) -> QWidget:
        """HTMLエディタを作成"""
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        label = QLabel("HTML編集")
        label.setStyleSheet("""
            padding: 4px 8px;
            background-color: #fff3e0;
            font-weight: bold;
            font-size: 11px;
            color: #e65100;
            border-bottom: 1px solid #ff9800;
        """)
        label.setFixedHeight(24)
        editor_layout.addWidget(label)
        
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText(
            "HTMLで入力...\n\n"
            "例:\n"
            "<p>次の方程式を解け。</p>\n"
            "$$x^2 + 2x + 1 = 0$$"
        )
        
        font = QFont("Courier New", 12)
        self.text_editor.setFont(font)
        self.text_editor.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: none;
                padding: 10px;
                line-height: 1.5;
            }
        """)
        
        self.text_editor.textChanged.connect(self.on_text_changed)
        
        editor_layout.addWidget(self.text_editor)
        
        return editor_widget
    
    def create_preview(self) -> QWidget:
        """プレビューエリアを作成"""
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)
        
        label = QLabel("プレビュー")
        label.setStyleSheet("""
            padding: 4px 8px;
            background-color: #e8f5e9;
            font-weight: bold;
            font-size: 11px;
            color: #388e3c;
            border-bottom: 1px solid #4caf50;
        """)
        label.setFixedHeight(24)
        preview_layout.addWidget(label)
        
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("""
            QWebEngineView {
                background-color: #ffffff;
                border: none;
            }
        """)
        
        self.web_view.loadFinished.connect(self._on_load_finished)
        
        preview_layout.addWidget(self.web_view)
        
        return preview_widget
    
    def _set_initial_html(self):
        """初期HTMLを設定"""
        initial_html = self._wrap_html("<p>左側のエディタにHTMLを入力すると、ここにプレビューが表示されます。</p>")
        self.web_view.setHtml(initial_html)
    
    def _on_load_finished(self, ok):
        """ページロード完了時の処理"""
        if ok:
            self._restore_scroll_position()
    
    def insert_html(self, prefix: str, suffix: str):
        """HTMLタグを挿入"""
        cursor = self.text_editor.textCursor()
        
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cursor.insertText(prefix + selected_text + suffix)
        else:
            position = cursor.position()
            cursor.insertText(prefix + suffix)
            cursor.setPosition(position + len(prefix))
            self.text_editor.setTextCursor(cursor)
        
        self.text_editor.setFocus()
    
    def insert_table(self):
        """表を挿入"""
        table_html = """
<table border="1">
  <tr>
    <th>項目1</th>
    <th>項目2</th>
  </tr>
  <tr>
    <td>内容1</td>
    <td>内容2</td>
  </tr>
</table>
"""
        cursor = self.text_editor.textCursor()
        cursor.insertText(table_html)
        self.text_editor.setFocus()
    
    def on_text_changed(self):
        """テキスト変更時の処理"""
        text = self.text_editor.toPlainText()
        self.text_changed.emit(text)
        
        self._save_scroll_position()
        
        self.update_timer.stop()
        self.update_timer.start(800)
    
    def _save_scroll_position(self):
        """現在のスクロール位置を保存"""
        self.web_view.page().runJavaScript(
            "window.pageYOffset",
            lambda result: setattr(self, 'scroll_position', result if result else 0)
        )
    
    def _restore_scroll_position(self):
        """スクロール位置を復元"""
        if self.scroll_position > 0:
            self.web_view.page().runJavaScript(
                f"window.scrollTo(0, {self.scroll_position});"
            )
    
    def _do_update_preview(self):
        """実際のプレビュー更新処理"""
        text = self.text_editor.toPlainText()
        
        if not text.strip():
            self._set_initial_html()
            return
        
        try:
            html = self._wrap_html(text)
            self._save_scroll_position()
            self.web_view.setHtml(html)
            
            QTimer.singleShot(100, self._retypeset_mathjax)
        except Exception as e:
            print(f"プレビュー更新エラー: {e}")
    
    def _retypeset_mathjax(self):
        """MathJaxの再処理"""
        self.web_view.page().runJavaScript("""
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
                MathJax.typesetPromise().catch((err) => console.log(err));
            }
        """)
        QTimer.singleShot(200, self._restore_scroll_position)
    
    def _wrap_html(self, content: str) -> str:
        """HTMLをラップ"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: true
            }}
        }};
    </script>
    <style>
        body {{
            font-family: 'MS Mincho', 'Hiragino Mincho ProN', serif;
            font-size: 12pt;
            line-height: 1.8;
            padding: 15px 20px;
            color: #000;
        }}
        p {{ margin: 1em 0; }}
        table {{
            border-collapse: collapse;
            margin: 1em 0;
            border: 2px solid #000;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 10px;
        }}
        th {{ font-weight: bold; }}
    </style>
</head>
<body>
{content}
</body>
</html>'''
    
    def get_text(self) -> str:
        """エディタのテキストを取得"""
        return self.text_editor.toPlainText()
    
    def set_text(self, text: str):
        """エディタのテキストを設定"""
        self.text_editor.setPlainText(text)
