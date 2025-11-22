# -*- coding: utf-8 -*-
"""解答用紙生成ユーティリティ"""

import re
from typing import List, Dict, Tuple


class AnswerSheetGenerator:
    """解答用紙生成クラス"""
    
    # 空欄パターン（カタカナ1文字）
    BLANK_PATTERN = r'[ア-ン]'
    
    # 数字の空欄パターン（数字1-2桁）
    NUMBER_BLANK_PATTERN = r'(?:①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮|⑯|⑰|⑱|⑲|⑳)'
    
    def __init__(self):
        pass
    
    def extract_blanks(self, content: str) -> List[str]:
        """問題文から空欄を抽出
        
        Args:
            content: 問題文の内容
        
        Returns:
            抽出された空欄のリスト（順序を保持、重複除去）
        """
        # カタカナの空欄を検索
        blanks = []
        seen = set()
        
        # カタカナ空欄
        for match in re.finditer(self.BLANK_PATTERN, content):
            blank = match.group()
            if blank not in seen:
                blanks.append(blank)
                seen.add(blank)
        
        # 丸数字空欄
        for match in re.finditer(self.NUMBER_BLANK_PATTERN, content):
            blank = match.group()
            if blank not in seen:
                blanks.append(blank)
                seen.add(blank)
        
        return blanks
    
    def generate_answer_sheet_html(self, problems: List, options: dict = None) -> str:
        """解答用紙のHTMLを生成
        
        Args:
            problems: 問題リスト
            options: エクスポートオプション
        
        Returns:
            解答用紙のHTML
        """
        if options is None:
            options = {}
        
        html = '<div class="answer-sheet-page">'
        html += '<h1 class="answer-sheet-title">解答用紙</h1>'
        html += '<div class="student-info-answer">'
        html += '<table class="info-table">'
        html += '<tr><td class="label">受験番号</td><td class="field-answer"></td></tr>'
        html += '<tr><td class="label">氏名</td><td class="field-answer"></td></tr>'
        html += '</table>'
        html += '</div>'
        
        # 日本語の問題番号変換
        japanese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        for i, problem in enumerate(problems, 1):
            blanks = self.extract_blanks(problem.content)
            
            if not blanks:
                continue
            
            # 問題番号
            if i <= len(japanese_numbers):
                problem_title = f'第{japanese_numbers[i-1]}問'
            else:
                problem_title = f'第{i}問'
            
            # 配点
            score_display = ''
            if hasattr(problem, 'score') and problem.score:
                score_display = f'（{problem.score}点）'
            
            html += f'<div class="answer-section">'
            html += f'<h2 class="answer-problem-title">{problem_title} {score_display}</h2>'
            html += '<table class="answer-table">'
            
            # 空欄を4列で表示
            for j in range(0, len(blanks), 4):
                html += '<tr>'
                for k in range(4):
                    if j + k < len(blanks):
                        blank = blanks[j + k]
                        html += f'<td class="blank-label">{blank}</td>'
                        html += '<td class="blank-field"></td>'
                    else:
                        html += '<td></td><td></td>'
                html += '</tr>'
            
            html += '</table>'
            html += '</div>'
        
        html += '</div>'
        return html
    
    def get_answer_sheet_styles(self) -> str:
        """解答用紙のスタイルを取得"""
        return """
        /* 解答用紙スタイル */
        .answer-sheet-page {
            min-height: 100vh;
            padding: 25mm 20mm;
        }
        
        .answer-sheet-title {
            font-size: 24pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }
        
        .student-info-answer {
            margin-bottom: 40px;
        }
        
        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .info-table td {
            border: 1px solid #000;
            padding: 12px;
        }
        
        .info-table .label {
            width: 20%;
            font-weight: bold;
            background-color: #f5f5f5;
        }
        
        .info-table .field-answer {
            width: 80%;
            height: 40px;
        }
        
        .answer-section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }
        
        .answer-problem-title {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 15px;
            padding: 8px;
            background-color: #f0f0f0;
            border-left: 4px solid #000;
        }
        
        .answer-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .answer-table td {
            border: 1px solid #000;
            padding: 10px;
        }
        
        .answer-table .blank-label {
            width: 10%;
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            background-color: #f8f8f8;
        }
        
        .answer-table .blank-field {
            width: 15%;
            height: 35px;
        }
        
        @media print {
            .answer-sheet-page {
                page-break-before: always;
            }
        }
        """
