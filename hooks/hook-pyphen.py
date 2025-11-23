# -*- coding: utf-8 -*-
"""
PyInstaller hook for pyphen
"""

from PyInstaller.utils.hooks import collect_data_files

# pyphenの辞書ファイルを収集
datas = collect_data_files('pyphen')
