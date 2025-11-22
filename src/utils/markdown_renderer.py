# -*- coding: utf-8 -*-
"""マークダウンレンダラー"""

import re
import markdown


class MarkdownRenderer:
    """マークダウンをHTMLに変換するクラス"""
    
    def __init__(self):
        self.md = markdown.Markdown(
            extensions=[
                'extra',
                'nl2br',
                'sane_lists'
            ]
        )
        self.math_blocks = []
    
    def render(self, text: str) -> str:
        """マークダウンをHTMLに変換"""
        protected_text, self.math_blocks = self._protect_math(text)
        html = self.md.convert(protected_text)
        html = self._restore_math(html)
        return self._wrap_html(html)
    
    def _protect_math(self, text: str) -> tuple:
        """数式を保護"""
        math_blocks = []
        code_blocks = []
        
        # 1. まずコードブロックを保護（数式が含まれている場合）
        def replace_code_block(match):
            index = len(code_blocks)
            code_blocks.append(match.group(0))
            return f'CODEBLOCK{index}CODEBLOCK'
        
        # ```で囲まれたコードブロックを保護
        text = re.sub(r'```[\s\S]*?```', replace_code_block, text)
        
        # 2. ディスプレイ数式を保護
        def replace_display(match):
            index = len(math_blocks)
            math_blocks.append(('display', match.group(1)))
            return f'MATHBLOCK{index}MATHBLOCK'
        
        text = re.sub(r'\$\$(.*?)\$\$', replace_display, text, flags=re.DOTALL)
        
        # 3. インライン数式を保護
        def replace_inline(match):
            index = len(math_blocks)
            math_blocks.append(('inline', match.group(1)))
            return f'MATHBLOCK{index}MATHBLOCK'
        
        text = re.sub(r'\$([^\$\n]+?)\$', replace_inline, text)
        
        # コードブロックを復元（数式保護後）
        for i, code_block in enumerate(code_blocks):
            text = text.replace(f'CODEBLOCK{i}CODEBLOCK', code_block)
        
        return text, math_blocks
    
    def _restore_math(self, html: str) -> str:
        """数式を復元"""
        for i, (math_type, content) in enumerate(self.math_blocks):
            placeholder = f'MATHBLOCK{i}MATHBLOCK'
            if math_type == 'display':
                # ディスプレイ数式: $$...$$形式で復元（MathJaxが処理）
                math_html = f'<div class="math-display">$$\n{content}\n$$</div>'
            else:
                # インライン数式: $...$形式で復元（MathJaxが処理）
                math_html = f'<span class="math-inline">${content}$</span>'
            html = html.replace(placeholder, math_html)
        
        return html
    
    def _wrap_html(self, content: str) -> str:
        """HTMLをラップしてスタイルを適用"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                        console.log('MathJax initialization complete');
                    }});
                }}
            }}
        }};
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'MS Mincho', 'Hiragino Mincho ProN', serif;
            font-size: 12pt;
            line-height: 1.8;
            padding: 15px 20px;
            background-color: #ffffff;
            color: #000000;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #000000;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            font-weight: bold;
        }}
        h1 {{ font-size: 1.6em; }}
        h2 {{ font-size: 1.4em; }}
        h3 {{ font-size: 1.2em; }}
        p {{ margin: 1em 0; text-indent: 1em; }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border: 1px solid #000;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 12px;
            border: 1px solid #000;
            overflow-x: auto;
            margin: 1em 0;
        }}
        pre code {{ background-color: transparent; padding: 0; border: none; }}
        blockquote {{
            border-left: 3px solid #000;
            padding-left: 15px;
            margin: 1em 0;
        }}
        ul, ol {{ margin: 1em 0; padding-left: 2em; }}
        li {{ margin: 0.5em 0; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            border: 2px solid #000;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 10px;
            text-align: left;
        }}
        th {{ font-weight: bold; }}
        .math-display {{
            margin: 1.5em 0;
            text-align: center;
            overflow-x: auto;
        }}
        .math-inline {{ display: inline; }}
        hr {{ border: none; border-top: 1px solid #000; margin: 1.5em 0; }}
        a {{ color: #000; text-decoration: underline; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
{content}
</body>
</html>'''
