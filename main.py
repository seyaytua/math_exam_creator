#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Math Exam Creator - メインエントリーポイント """

import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# srcディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main_window import MainWindow


def main():
    """メインアプリケーション"""
    # High DPI対応
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Math Exam Creator")
    app.setOrganizationName("MathExamCreator")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()