"""HTML出力機能"""

from pathlib import Path
from typing import List
from datetime import datetime
from ..models import Project, Problem
from ..utils import MarkdownRenderer, AnswerSheetGenerator


class HTMLExporter:
    """HTMLエクスポーター"""
    
    def __init__(self):
        self.renderer = MarkdownRenderer()
        self.answer_generator = AnswerSheetGenerator()
    
    def export(self, project: Project, output_path: Path, options: dict = None):
        """プロジェクトをHTMLファイルとして出力（プラットフォーム互換）"""
        if options is None:
            options = {}
        
        html = self._generate_html(project, options)
        
        # UTF-8 で保存（改行コード統一、Windows 互換）
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
    
    def _generate_html(self, project: Project, options: dict) -> str:
        """HTML生成"""
        cover_html = self._generate_cover(project, options)
        problems_html = self._generate_problems(project.problems, options)
        
        # 解答用紙を生成（オプションで有効な場合）
        answer_sheet_html = ''
        if options.get('generate_answer_sheet', False):
            answer_sheet_html = self.answer_generator.generate_answer_sheet_html(
                project.problems, options
            )
        
        return self._wrap_document(cover_html, problems_html, answer_sheet_html, project, options)
    
    def _generate_cover(self, project: Project, options: dict) -> str:
        """表紙生成"""
        show_cover = options.get('show_cover', True)
        if not show_cover:
            return ""
        
        title = options.get('exam_title', project.title) or project.title
        subtitle = options.get('exam_subtitle', '') or ''
        date = options.get('exam_date', '') or ''
        school = options.get('school_name', '') or ''
        grade = options.get('grade', '') or ''
        subject = options.get('subject', '数学') or '数学'
        time_limit = options.get('time_limit', '') or ''
        total_score = options.get('total_score', '') or ''
        notes = options.get('notes', '') or ''
        
        cover_html = f'''
        <div class="cover-page">
            <div class="cover-content">
                <h1 class="exam-title">{title}</h1>
                {f'<p class="exam-subtitle">{subtitle}</p>' if subtitle else ''}
                <div class="exam-info">
                    {f'<p class="school-name">{school}</p>' if school else ''}
                    {f'<p class="grade">{grade}</p>' if grade else ''}
                    <p class="subject">{subject}</p>
                    {f'<p class="date">{date}</p>' if date else ''}
                </div>
                <div class="exam-details">
                    {f'<p>試験時間　{time_limit}</p>' if time_limit else ''}
                    {f'<p>配点　{total_score}</p>' if total_score else ''}
                </div>
                {f'<div class="exam-notes"><pre>{notes}</pre></div>' if notes else ''}
                <div class="student-info">
                    <table>
                        <tr>
                            <td class="label">受験番号</td>
                            <td class="field"></td>
                        </tr>
                        <tr>
                            <td class="label">氏名</td>
                            <td class="field"></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <div class="page-break"></div>
        '''
        
        return cover_html
    
    def _generate_problems(self, problems: List[Problem], options: dict) -> str:
        """問題生成（1-2問/ページ）"""
        problems_html = ''
        
        show_problem_numbers = options.get('show_problem_numbers', True)
        problems_per_page = options.get('problems_per_page', 1)
        
        # 日本語の問題番号変換
        japanese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        for i, problem in enumerate(problems, 1):
            problem_html = self.renderer.render(problem.content)
            
            import re
            body_match = re.search(r'<body>(.*?)</body>', problem_html, re.DOTALL)
            if body_match:
                problem_content = body_match.group(1)
            else:
                problem_content = problem_html
            
            if (i - 1) % problems_per_page == 0:
                problems_html += '<div class="problem-page">'
            
            if show_problem_numbers:
                # 日本語の問題番号を生成
                if i <= len(japanese_numbers):
                    problem_title = f'第{japanese_numbers[i-1]}問'
                else:
                    problem_title = f'第{i}問'
                
                # 問題タイトルから配点を抽出（Problem.titleに格納されている場合）
                problem_obj = problems[i-1]
                score_display = ''
                if hasattr(problem_obj, 'score') and problem_obj.score:
                    score_display = f'（配点　{problem_obj.score}）'
                
                # 必答・選択の区別
                problem_type_display = ''
                if hasattr(problem_obj, 'problem_type'):
                    if problem_obj.problem_type == 'required':
                        problem_type_display = '（必答問題）'
                    elif problem_obj.problem_type == 'optional':
                        problem_type_display = '（選択問題）'
                
                problems_html += f'''
                <div class="problem-container">
                    <div class="problem-header">
                        <h2 class="problem-title">{problem_title} {problem_type_display}</h2>
                        {f'<span class="problem-score">{score_display}</span>' if score_display else ''}
                    </div>
                    <div class="problem-content">
                        {problem_content}
                    </div>
                </div>
                '''
            else:
                problems_html += f'''
                <div class="problem-container">
                    <div class="problem-content">
                        {problem_content}
                    </div>
                </div>
                '''
            
            if i % problems_per_page == 0 or i == len(problems):
                problems_html += '</div>'
                if i < len(problems):
                    problems_html += '<div class="page-break"></div>'
        
        return problems_html
    
    def _wrap_document(self, cover_html: str, problems_html: str, 
                       answer_sheet_html: str, project: Project, options: dict) -> str:
        """完全なHTMLドキュメントを生成"""
        font_size = options.get('font_size', 12)
        line_spacing = options.get('line_spacing', 1.8)
        margin = options.get('margin', '20mm')
        page_size = options.get('page_size', 'A4')
        
        return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project.title}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: true,
                packages: {{'[+]': ['noerrors']}}
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }},
            startup: {{
                pageReady: () => {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax loaded successfully');
                    }});
                }}
            }}
        }};
    </script>
    <style>
        @media print {{
            .page-break {{
                page-break-after: always;
                break-after: page;
            }}
            
            @page {{
                size: {page_size};
                margin: {margin};
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'MS Mincho', 'Hiragino Mincho ProN', serif;
            font-size: {font_size}pt;
            line-height: {line_spacing};
            color: #000;
            background-color: #fff;
        }}
        
        /* 表紙スタイル */
        .cover-page {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px;
        }}
        
        .cover-content {{
            width: 100%;
            max-width: 500px;
            border: 3px solid #000;
            padding: 50px 30px;
        }}
        
        .exam-title {{
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 30px;
            letter-spacing: 0.2em;
        }}
        
        .exam-subtitle {{
            font-size: 14pt;
            margin-bottom: 40px;
        }}
        
        .exam-info {{
            margin: 40px 0;
            font-size: 12pt;
        }}
        
        .exam-info p {{
            margin: 8px 0;
        }}
        
        .school-name {{
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .exam-details {{
            margin: 40px 0;
            padding: 20px;
            border: 2px solid #000;
            text-align: left;
        }}
        
        .exam-details p {{
            margin: 8px 0;
            font-size: 11pt;
        }}
        
        .exam-notes {{
            margin: 30px 0;
            padding: 15px;
            border: 1px solid #000;
            text-align: left;
        }}
        
        .exam-notes pre {{
            white-space: pre-wrap;
            font-family: inherit;
            font-size: 10pt;
            line-height: 1.6;
        }}
        
        .student-info {{
            margin-top: 60px;
        }}
        
        .student-info table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .student-info td {{
            border: 1px solid #000;
            padding: 12px;
            font-size: 11pt;
        }}
        
        .student-info .label {{
            width: 30%;
            font-weight: bold;
            background-color: #fff;
        }}
        
        .student-info .field {{
            width: 70%;
            height: 40px;
        }}
        
        /* 問題ページスタイル */
        .problem-page {{
            min-height: 100vh;
            padding: 25mm 20mm;
        }}
        
        .problem-container {{
            margin-bottom: 50px;
        }}
        
        .problem-header {{
            margin-bottom: 20px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }}
        
        .problem-title {{
            font-size: 18pt;
            font-weight: bold;
            display: inline-block;
            margin: 0;
            padding: 0;
        }}
        
        .problem-score {{
            font-size: 12pt;
            margin-left: 20px;
        }}
        
        .problem-content {{
            padding: 20px 5px;
        }}
        
        /* マークダウンコンテンツスタイル */
        .problem-content h1,
        .problem-content h2,
        .problem-content h3 {{
            color: #000;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            font-weight: bold;
        }}
        
        .problem-content h1 {{ font-size: 1.4em; }}
        .problem-content h2 {{ font-size: 1.2em; }}
        .problem-content h3 {{ font-size: 1.1em; }}
        
        .problem-content p {{
            margin: 1.2em 0;
            text-indent: 1em;
        }}
        
        .problem-content ul,
        .problem-content ol {{
            margin: 1.2em 0;
            padding-left: 2em;
        }}
        
        .problem-content li {{
            margin: 0.8em 0;
        }}
        
        .problem-content code {{
            font-family: 'Courier New', monospace;
            border: 1px solid #000;
            padding: 2px 6px;
        }}
        
        .problem-content pre {{
            border: 1px solid #000;
            padding: 15px;
            overflow-x: auto;
            margin: 1.2em 0;
            background-color: #fff;
        }}
        
        .problem-content table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            border: 2px solid #000;
        }}
        
        .problem-content th,
        .problem-content td {{
            border: 1px solid #000;
            padding: 10px;
            text-align: left;
        }}
        
        .problem-content th {{
            font-weight: bold;
            background-color: #fff;
        }}
        
        .problem-content blockquote {{
            border-left: 3px solid #000;
            padding-left: 15px;
            margin: 1.2em 0;
        }}
        
        /* 数式スタイル */
        .math-display {{
            margin: 1.5em 0;
            text-align: center;
            overflow-x: auto;
        }}
        
        .math-inline {{
            display: inline;
            vertical-align: middle;
        }}
        
        /* MathJax出力の調整 */
        .MathJax {{
            font-size: 110% !important;
        }}
        
        mjx-container[display="true"] {{
            margin: 1.5em 0 !important;
        }}
        
        /* ページ区切り */
        .page-break {{
            page-break-after: always;
            break-after: page;
        }}
        
        /* 印刷時の調整 */
        @media print {{
            body {{
                font-size: 11pt;
            }}
            
            .problem-page {{
                padding: 20mm 15mm;
            }}
        }}
        
        {self.answer_generator.get_answer_sheet_styles() if answer_sheet_html else ''}
    </style>
</head>
<body>
    {cover_html}
    {problems_html}
    {answer_sheet_html}
</body>
</html>'''