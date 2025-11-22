# -*- coding: utf-8 -*-
"""PDF出力機能"""

from pathlib import Path
from typing import Optional
from ..models import Project

# PDF生成ライブラリの動的インポート
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from xhtml2pdf import pisa
    XHTML2PDF_AVAILABLE = True
except ImportError:
    XHTML2PDF_AVAILABLE = False


class PDFExporter:
    """PDFエクスポーター"""
    
    def __init__(self):
        self.html_exporter = None
    
    def is_available(self) -> tuple:
        """PDF出力が利用可能かチェック
        
        Returns:
            (利用可能か, 利用可能なライブラリ名)
        """
        if WEASYPRINT_AVAILABLE:
            return (True, "weasyprint")
        elif XHTML2PDF_AVAILABLE:
            return (True, "xhtml2pdf")
        else:
            return (False, None)
    
    def export_with_weasyprint(self, html_content: str, output_path: Path):
        """WeasyprintでPDF出力
        
        Args:
            html_content: HTML文字列
            output_path: 出力先パス
        """
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("weasyprintがインストールされていません")
        
        # HTMLからPDFを生成
        HTML(string=html_content).write_pdf(output_path)
    
    def export_with_xhtml2pdf(self, html_content: str, output_path: Path):
        """xhtml2pdfでPDF出力
        
        Args:
            html_content: HTML文字列
            output_path: 出力先パス
        """
        if not XHTML2PDF_AVAILABLE:
            raise ImportError("xhtml2pdfがインストールされていません")
        
        with open(output_path, 'wb') as output_file:
            pisa_status = pisa.CreatePDF(
                html_content.encode('utf-8'),
                dest=output_file,
                encoding='utf-8'
            )
            
            if pisa_status.err:
                raise Exception(f"PDF生成中にエラーが発生しました: {pisa_status.err}")
    
    def export(self, project: Project, output_path: Path, options: dict = None):
        """プロジェクトをPDFファイルとして出力
        
        Args:
            project: プロジェクト
            output_path: 出力先パス
            options: エクスポートオプション
        """
        if options is None:
            options = {}
        
        # HTMLExporterを遅延インポート（循環インポート回避）
        if self.html_exporter is None:
            from .html_exporter import HTMLExporter
            self.html_exporter = HTMLExporter()
        
        # まずHTMLを生成
        html_content = self.html_exporter._generate_html(project, options)
        
        # 利用可能なライブラリでPDF出力
        available, library = self.is_available()
        
        if not available:
            raise ImportError(
                "PDF出力には以下のいずれかのライブラリが必要です:\n"
                "  pip install weasyprint\n"
                "または\n"
                "  pip install xhtml2pdf"
            )
        
        if library == "weasyprint":
            self.export_with_weasyprint(html_content, output_path)
        elif library == "xhtml2pdf":
            self.export_with_xhtml2pdf(html_content, output_path)
    
    def get_install_instructions(self) -> str:
        """インストール手順を取得"""
        return """
PDF出力機能を使用するには、以下のいずれかをインストールしてください:

【推奨】WeasyPrint（高品質PDF生成）:
  pip install weasyprint

または

xhtml2pdf（軽量PDF生成）:
  pip install xhtml2pdf

※ WeasyprintはGTK+などの依存関係が必要な場合があります。
  macOS: brew install cairo pango gdk-pixbuf libffi
  Ubuntu/Debian: sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
        """
