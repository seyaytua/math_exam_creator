# -*- coding: utf-8 -*-
"""
PyInstaller hook for cairocffi
"""

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# cairocffiの動的ライブラリを収集
binaries = collect_dynamic_libs('cairocffi')

# cairocffiのデータファイルを収集
datas = collect_data_files('cairocffi')
