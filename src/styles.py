# -*- coding: utf-8 -*-
"""スタイルシート定義"""


class Styles:
    """アプリケーションのスタイルシートを管理するクラス"""
    
    @staticmethod
    def get_main_stylesheet() -> str:
        """メインウィンドウのスタイルシートを取得
        
        Returns:
            スタイルシート文字列
        """
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 4px;
            }
            
            QMenuBar::item {
                padding: 4px 8px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #e3f2fd;
            }
            
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
            }
            
            QMenu::item {
                padding: 6px 24px 6px 8px;
            }
            
            QMenu::item:selected {
                background-color: #e3f2fd;
            }
            
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                spacing: 4px;
                padding: 4px;
            }
            
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
            }
            
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid #ffffff;
            }
            
            QTabBar::tab:hover {
                background-color: #e3f2fd;
            }
            
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e0e0e0;
            }
            
            QLabel {
                color: #333333;
            }
            
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
            }
            
            QPushButton:hover {
                background-color: #1976d2;
            }
            
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            
            QTextEdit, QPlainTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12pt;
            }
        """