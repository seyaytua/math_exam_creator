# -*- coding: utf-8 -*-
"""エクスポーターパッケージ"""

from .html_exporter import HTMLExporter

# PDF Exporterはオプショナル（依存関係がインストールされている場合のみ）
try:
    from .pdf_exporter import PDFExporter
    __all__ = ['HTMLExporter', 'PDFExporter']
except (ImportError, OSError) as e:
    # WeasyPrintの依存関係が見つからない場合
    PDFExporter = None
    __all__ = ['HTMLExporter']
    import warnings
    warnings.warn(
        f"PDF出力機能が利用できません: {str(e)}\n"
        "PDF出力を使用するには、以下のコマンドを実行してください:\n"
        "  brew install cairo pango gdk-pixbuf libffi\n"
        "  pip3 install --upgrade weasyprint",
        ImportWarning
    )
