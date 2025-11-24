# -*- coding: utf-8 -*-
"""表紙編集ウィジェット"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QLabel, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class CoverEditor(QWidget):
    """表紙編集ウィジェット"""
    
    content_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # タイトル
        title_label = QLabel("表紙設定")
        title_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #2196f3;
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # 基本情報グループ
        basic_group = QGroupBox("基本情報")
        basic_layout = QFormLayout()
        basic_layout.setSpacing(10)
        
        self.exam_title_edit = QLineEdit()
        self.exam_title_edit.setPlaceholderText("例: 第1回定期考査")
        self.exam_title_edit.textChanged.connect(lambda: self.content_changed.emit())
        basic_layout.addRow("試験名:", self.exam_title_edit)
        
        self.exam_subtitle_edit = QLineEdit()
        self.exam_subtitle_edit.setPlaceholderText("例: 中間試験")
        self.exam_subtitle_edit.textChanged.connect(lambda: self.content_changed.emit())
        basic_layout.addRow("サブタイトル:", self.exam_subtitle_edit)
        
        self.subject_edit = QLineEdit()
        self.subject_edit.setText("数学")
        self.subject_edit.textChanged.connect(lambda: self.content_changed.emit())
        basic_layout.addRow("科目:", self.subject_edit)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 学校情報グループ
        school_group = QGroupBox("学校情報")
        school_layout = QFormLayout()
        school_layout.setSpacing(10)
        
        self.school_name_edit = QLineEdit()
        self.school_name_edit.setPlaceholderText("例: ○○高等学校")
        self.school_name_edit.textChanged.connect(lambda: self.content_changed.emit())
        school_layout.addRow("学校名:", self.school_name_edit)
        
        self.grade_edit = QLineEdit()
        self.grade_edit.setPlaceholderText("例: 高校1年")
        self.grade_edit.textChanged.connect(lambda: self.content_changed.emit())
        school_layout.addRow("学年:", self.grade_edit)
        
        school_group.setLayout(school_layout)
        layout.addWidget(school_group)
        
        # 試験情報グループ
        exam_group = QGroupBox("試験情報")
        exam_layout = QFormLayout()
        exam_layout.setSpacing(10)
        
        self.exam_date_edit = QLineEdit()
        self.exam_date_edit.setPlaceholderText("例: 2025年6月15日")
        self.exam_date_edit.textChanged.connect(lambda: self.content_changed.emit())
        exam_layout.addRow("実施日:", self.exam_date_edit)
        
        self.time_limit_edit = QLineEdit()
        self.time_limit_edit.setPlaceholderText("例: 50分")
        self.time_limit_edit.textChanged.connect(lambda: self.content_changed.emit())
        exam_layout.addRow("試験時間:", self.time_limit_edit)
        
        self.total_score_edit = QLineEdit()
        self.total_score_edit.setPlaceholderText("例: 100点")
        self.total_score_edit.textChanged.connect(lambda: self.content_changed.emit())
        exam_layout.addRow("配点:", self.total_score_edit)
        
        exam_group.setLayout(exam_layout)
        layout.addWidget(exam_group)
        
        # 注意事項グループ
        notes_group = QGroupBox("注意事項")
        notes_layout = QVBoxLayout()
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "試験の注意事項を入力してください。\n\n"
            "例:\n"
            "1. 解答はすべて解答用紙に記入すること。\n"
            "2. 計算機の使用は不可。\n"
            "3. 定規・コンパスの使用可。"
        )
        self.notes_edit.setMaximumHeight(150)
        self.notes_edit.textChanged.connect(lambda: self.content_changed.emit())
        notes_layout.addWidget(self.notes_edit)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def get_cover_data(self) -> dict:
        """表紙データを取得"""
        return {
            'exam_title': self.exam_title_edit.text(),
            'exam_subtitle': self.exam_subtitle_edit.text(),
            'subject': self.subject_edit.text(),
            'school_name': self.school_name_edit.text(),
            'grade': self.grade_edit.text(),
            'exam_date': self.exam_date_edit.text(),
            'time_limit': self.time_limit_edit.text(),
            'total_score': self.total_score_edit.text(),
            'notes': self.notes_edit.toPlainText()
        }
    
    def set_cover_data(self, data: dict):
        """表紙データを設定"""
        self.exam_title_edit.setText(data.get('exam_title', ''))
        self.exam_subtitle_edit.setText(data.get('exam_subtitle', ''))
        self.subject_edit.setText(data.get('subject', '数学'))
        self.school_name_edit.setText(data.get('school_name', ''))
        self.grade_edit.setText(data.get('grade', ''))
        self.exam_date_edit.setText(data.get('exam_date', ''))
        self.time_limit_edit.setText(data.get('time_limit', ''))
        self.total_score_edit.setText(data.get('total_score', ''))
        self.notes_edit.setPlainText(data.get('notes', ''))
    
    def undo(self):
        """元に戻す（注意事項欄のみ）"""
        # QLineEditにはUNDO機能があるが、フォーカスが必要
        # 現在フォーカスされているウィジェットでUNDOを実行
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.undo()
        elif isinstance(focused_widget, QTextEdit):
            focused_widget.undo()
    
    def redo(self):
        """やり直す"""
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.redo()
        elif isinstance(focused_widget, QTextEdit):
            focused_widget.redo()
    
    def can_undo(self) -> bool:
        """元に戻すが可能か"""
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            return focused_widget.isUndoAvailable()
        elif isinstance(focused_widget, QTextEdit):
            return focused_widget.document().isUndoAvailable()
        return False
    
    def can_redo(self) -> bool:
        """やり直すが可能か"""
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            return focused_widget.isRedoAvailable()
        elif isinstance(focused_widget, QTextEdit):
            return focused_widget.document().isRedoAvailable()
        return False
