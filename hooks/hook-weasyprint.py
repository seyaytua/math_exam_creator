# -*- coding: utf-8 -*-
"""
PyInstaller hook for WeasyPrint
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# WeasyPrintのすべてのサブモジュールを収集
hiddenimports = collect_submodules('weasyprint')

# WeasyPrintのデータファイルを収集
datas = collect_data_files('weasyprint')

# 依存ライブラリのサブモジュールも収集
hiddenimports += collect_submodules('cairocffi')
hiddenimports += collect_submodules('cairosvg')
hiddenimports += collect_submodules('cssselect2')
hiddenimports += collect_submodules('tinycss2')
hiddenimports += collect_submodules('pyphen')
hiddenimports += collect_submodules('fonttools')
