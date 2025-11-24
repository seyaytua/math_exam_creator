# -*- coding: utf-8 -*-
"""問題編集ウィジェット"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QLabel, QPushButton, QToolBar, QLineEdit, QFormLayout,
    QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QTimer, QUrl
from PySide6.QtGui import QFont, QTextOption, QAction, QTextCursor
from PySide6.QtWebEngineWidgets import QWebEngineView

from ..utils import MarkdownRenderer


class ProblemEditor(QWidget):
    """問題編集ウィジェット"""
    
    text_changed = Signal(str)
    score_changed = Signal(str)
    type_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = MarkdownRenderer()
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._do_update_preview)
        self.scroll_position = 0
        self.mathjax_loaded = False
        self.init_ui()
        self._set_initial_html()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 問題設定エリア
        settings_layout = QHBoxLayout()
        settings_layout.setContentsMargins(10, 5, 10, 5)
        
        # 配点入力フィールド
        score_label = QLabel("配点:")
        score_label.setStyleSheet("font-weight: bold;")
        self.score_edit = QLineEdit()
        self.score_edit.setPlaceholderText("例: 15 または 15点")
        self.score_edit.setMaximumWidth(150)
        self.score_edit.textChanged.connect(self.score_changed.emit)
        settings_layout.addWidget(score_label)
        settings_layout.addWidget(self.score_edit)
        
        settings_layout.addSpacing(20)
        
        # 必答・選択の区別
        type_label = QLabel("区分:")
        type_label.setStyleSheet("font-weight: bold;")
        settings_layout.addWidget(type_label)
        
        self.required_radio = QRadioButton("必答問題")
        self.required_radio.setChecked(True)
        self.optional_radio = QRadioButton("選択問題")
        
        self.type_button_group = QButtonGroup()
        self.type_button_group.addButton(self.required_radio, 0)
        self.type_button_group.addButton(self.optional_radio, 1)
        self.type_button_group.buttonClicked.connect(self._on_type_changed)
        
        settings_layout.addWidget(self.required_radio)
        settings_layout.addWidget(self.optional_radio)
        settings_layout.addStretch()
        layout.addLayout(settings_layout)
        
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
            QToolBar QToolButton:pressed {
                background-color: #bbdefb;
            }
        """)
        
        bold_action = QAction("太字 (Ctrl+B)", self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(lambda: self.insert_markdown("**", "**"))
        toolbar.addAction(bold_action)
        
        italic_action = QAction("斜体 (Ctrl+I)", self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(lambda: self.insert_markdown("*", "*"))
        toolbar.addAction(italic_action)
        
        toolbar.addSeparator()
        
        inline_math_action = QAction("インライン数式 (Ctrl+M)", self)
        inline_math_action.setShortcut("Ctrl+M")
        inline_math_action.triggered.connect(lambda: self.insert_markdown("$", "$"))
        toolbar.addAction(inline_math_action)
        
        display_math_action = QAction("ディスプレイ数式 (Ctrl+Shift+M)", self)
        display_math_action.setShortcut("Ctrl+Shift+M")
        display_math_action.triggered.connect(lambda: self.insert_markdown("\n$$\n", "\n$$\n"))
        toolbar.addAction(display_math_action)
        
        toolbar.addSeparator()
        
        heading_action = QAction("見出し", self)
        heading_action.triggered.connect(lambda: self.insert_markdown("## ", ""))
        toolbar.addAction(heading_action)
        
        list_action = QAction("リスト", self)
        list_action.triggered.connect(lambda: self.insert_markdown("- ", ""))
        toolbar.addAction(list_action)
        
        numbered_list_action = QAction("番号付きリスト", self)
        numbered_list_action.triggered.connect(lambda: self.insert_markdown("1. ", ""))
        toolbar.addAction(numbered_list_action)
        
        toolbar.addSeparator()
        
        image_action = QAction("画像を挿入", self)
        image_action.triggered.connect(self.insert_image)
        toolbar.addAction(image_action)
        
        parent_layout.addWidget(toolbar)
    
    def create_editor(self) -> QWidget:
        """マークダウンエディタを作成"""
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        label = QLabel("編集")
        label.setStyleSheet("""
            padding: 4px 8px;
            background-color: #e3f2fd;
            font-weight: bold;
            font-size: 11px;
            color: #1976d2;
            border-bottom: 1px solid #2196f3;
        """)
        label.setFixedHeight(24)
        editor_layout.addWidget(label)
        
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText(
            "マークダウンで入力...\n\n"
            "例:\n"
            "## 問題1\n"
            "次の方程式を解け。\n\n"
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
        initial_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
            padding: 20px;
            color: #999;
            text-align: center;
            font-size: 14pt;
        }
    </style>
</head>
<body>
    <p>左側のエディタに入力すると、ここにプレビューが表示されます。</p>
</body>
</html>
"""
        self.web_view.setHtml(initial_html)
    
    def _on_load_finished(self, ok):
        """ページロード完了時の処理"""
        if ok:
            self.mathjax_loaded = True
            self._restore_scroll_position()
    
    def insert_markdown(self, prefix: str, suffix: str):
        """マークダウン記法を挿入"""
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
            html = self.renderer.render(text)
            self._save_scroll_position()
            self.web_view.setHtml(html)
            
            # MathJaxの再処理を強制
            QTimer.singleShot(100, self._retypeset_mathjax)
        except Exception as e:
            print(f"プレビュー更新エラー: {e}")
            import traceback
            traceback.print_exc()
            # エラーが発生してもプレースホルダーを表示
            error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
            padding: 20px;
            color: #d32f2f;
            background-color: #ffebee;
        }}
        pre {{
            background-color: #fff;
            padding: 10px;
            border: 1px solid #e57373;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h3>プレビューエラー</h3>
    <p>{str(e)}</p>
    <pre>{traceback.format_exc()}</pre>
</body>
</html>
"""
            self.web_view.setHtml(error_html)
    
    def _retypeset_mathjax(self):
        """MathJaxの再処理"""
        self.web_view.page().runJavaScript("""
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
                MathJax.typesetPromise().catch((err) => console.log(err));
            }
        """)
        # スクロール位置を復元
        QTimer.singleShot(200, self._restore_scroll_position)
    
    def get_text(self) -> str:
        """エディタのテキストを取得"""
        return self.text_editor.toPlainText()
    
    def set_text(self, text: str):
        """エディタのテキストを設定"""
        self.text_editor.setPlainText(text)
    
    def get_score(self) -> str:
        """配点を取得"""
        return self.score_edit.text()
    
    def set_score(self, score: str):
        """配点を設定"""
        self.score_edit.setText(score)
    
    def get_problem_type(self) -> str:
        """問題タイプを取得"""
        return "required" if self.required_radio.isChecked() else "optional"
    
    def set_problem_type(self, problem_type: str):
        """問題タイプを設定"""
        if problem_type == "optional":
            self.optional_radio.setChecked(True)
        else:
            self.required_radio.setChecked(True)
    
    def _on_type_changed(self):
        """問題タイプ変更時の処理"""
        self.type_changed.emit(self.get_problem_type())
    
    def insert_image(self):
        """画像を挿入"""
        from ..dialogs import ImageInsertDialog
        
        dialog = ImageInsertDialog(self)
        if dialog.exec():
            image_markdown = dialog.get_image_markdown()
            if image_markdown:
                cursor = self.text_editor.textCursor()
                cursor.insertText("\n" + image_markdown + "\n")
                self.text_editor.setFocus()
    
    def undo(self):
        """元に戻す"""
        self.text_editor.undo()
    
    def redo(self):
        """やり直す"""
        self.text_editor.redo()
    
    def can_undo(self) -> bool:
        """元に戻すが可能か"""
        return self.text_editor.document().isUndoAvailable()
    
    def can_redo(self) -> bool:
        """やり直すが可能か"""
        return self.text_editor.document().isRedoAvailable()
