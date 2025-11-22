# -*- coding: utf-8 -*-
"""数式エディタダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QTabWidget, QWidget,
    QGridLayout, QGroupBox, QButtonGroup, QRadioButton,
    QLineEdit, QComboBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWebEngineWidgets import QWebEngineView


class MathEditorDialog(QDialog):
    """数式エディタダイアログ"""
    
    # 数式が確定したときのシグナル
    formula_accepted = Signal(str, str)  # (formula, mode)
    
    def __init__(self, parent=None, initial_formula="", mode="inline"):
        """
        Args:
            parent: 親ウィジェット
            initial_formula: 初期数式（LaTeX）
            mode: "inline" または "display"
        """
        super().__init__(parent)
        self.current_formula = initial_formula
        self.current_mode = mode
        self.setWindowTitle("数式エディタ")
        self.setMinimumSize(900, 700)
        self.init_ui()
        
        # 初期数式を設定
        if initial_formula:
            self.latex_edit.setPlainText(initial_formula)
            self.update_preview()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # モード選択
        mode_layout = QHBoxLayout()
        mode_label = QLabel("数式モード:")
        mode_layout.addWidget(mode_label)
        
        self.inline_radio = QRadioButton("インライン数式 ($...$)")
        self.display_radio = QRadioButton("ディスプレイ数式 ($$...$$)")
        
        if self.current_mode == "inline":
            self.inline_radio.setChecked(True)
        else:
            self.display_radio.setChecked(True)
        
        self.inline_radio.toggled.connect(self.on_mode_changed)
        
        mode_layout.addWidget(self.inline_radio)
        mode_layout.addWidget(self.display_radio)
        mode_layout.addStretch()
        
        layout.addLayout(mode_layout)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        
        # 1. 基本タブ
        basic_tab = self.create_basic_tab()
        self.tab_widget.addTab(basic_tab, "基本")
        
        # 2. 演算子タブ
        operators_tab = self.create_operators_tab()
        self.tab_widget.addTab(operators_tab, "演算子")
        
        # 3. ギリシャ文字タブ
        greek_tab = self.create_greek_tab()
        self.tab_widget.addTab(greek_tab, "ギリシャ文字")
        
        # 4. 関数タブ
        functions_tab = self.create_functions_tab()
        self.tab_widget.addTab(functions_tab, "関数")
        
        # 5. その他タブ
        misc_tab = self.create_misc_tab()
        self.tab_widget.addTab(misc_tab, "その他")
        
        layout.addWidget(self.tab_widget)
        
        # LaTeX入力エリア
        latex_group = QGroupBox("LaTeX コード")
        latex_layout = QVBoxLayout()
        
        self.latex_edit = QTextEdit()
        self.latex_edit.setFont(QFont("Courier New", 12))
        self.latex_edit.setMaximumHeight(100)
        self.latex_edit.textChanged.connect(self.update_preview)
        latex_layout.addWidget(self.latex_edit)
        
        latex_group.setLayout(latex_layout)
        layout.addWidget(latex_group)
        
        # プレビューエリア
        preview_group = QGroupBox("プレビュー")
        preview_layout = QVBoxLayout()
        
        self.preview_view = QWebEngineView()
        self.preview_view.setMinimumHeight(150)
        preview_layout.addWidget(self.preview_view)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        clear_button = QPushButton("クリア")
        clear_button.clicked.connect(self.clear_formula)
        button_layout.addWidget(clear_button)
        
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        insert_button = QPushButton("挿入")
        insert_button.setDefault(True)
        insert_button.clicked.connect(self.accept_formula)
        insert_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        button_layout.addWidget(insert_button)
        
        layout.addLayout(button_layout)
        
        # 初期プレビュー
        self.update_preview()
    
    def create_basic_tab(self):
        """基本タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 基本的な数式構造
        structures_group = QGroupBox("基本構造")
        structures_layout = QGridLayout()
        
        structures = [
            ("分数", r"\frac{a}{b}"),
            ("上付き", r"x^{2}"),
            ("下付き", r"x_{i}"),
            ("上下付き", r"x_{i}^{2}"),
            ("平方根", r"\sqrt{x}"),
            ("n乗根", r"\sqrt[n]{x}"),
            ("括弧", r"\left( x \right)"),
            ("中括弧", r"\left\{ x \right\}"),
            ("角括弧", r"\left[ x \right]"),
            ("絶対値", r"\left| x \right|"),
            ("二項係数", r"\binom{n}{k}"),
            ("行列", r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}"),
        ]
        
        row, col = 0, 0
        for label, latex in structures:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            structures_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        structures_group.setLayout(structures_layout)
        layout.addWidget(structures_group)
        
        layout.addStretch()
        return widget
    
    def create_operators_tab(self):
        """演算子タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 積分・総和
        calculus_group = QGroupBox("微積分")
        calculus_layout = QGridLayout()
        
        calculus = [
            ("積分", r"\int"),
            ("定積分", r"\int_{a}^{b}"),
            ("二重積分", r"\iint"),
            ("三重積分", r"\iiint"),
            ("周回積分", r"\oint"),
            ("総和", r"\sum"),
            ("総和(範囲)", r"\sum_{i=1}^{n}"),
            ("総積", r"\prod"),
            ("総積(範囲)", r"\prod_{i=1}^{n}"),
            ("極限", r"\lim"),
            ("極限(x→a)", r"\lim_{x \to a}"),
            ("微分", r"\frac{d}{dx}"),
            ("偏微分", r"\frac{\partial}{\partial x}"),
        ]
        
        row, col = 0, 0
        for label, latex in calculus:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            calculus_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        calculus_group.setLayout(calculus_layout)
        layout.addWidget(calculus_group)
        
        # 比較演算子
        comparison_group = QGroupBox("比較・論理")
        comparison_layout = QGridLayout()
        
        comparison = [
            ("≤", r"\leq"),
            ("≥", r"\geq"),
            ("≠", r"\neq"),
            ("≈", r"\approx"),
            ("≡", r"\equiv"),
            ("∈", r"\in"),
            ("∉", r"\notin"),
            ("⊂", r"\subset"),
            ("⊃", r"\supset"),
            ("∩", r"\cap"),
            ("∪", r"\cup"),
            ("∧", r"\wedge"),
            ("∨", r"\vee"),
            ("¬", r"\neg"),
            ("∀", r"\forall"),
            ("∃", r"\exists"),
        ]
        
        row, col = 0, 0
        for label, latex in comparison:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            comparison_layout.addWidget(btn, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        comparison_group.setLayout(comparison_layout)
        layout.addWidget(comparison_group)
        
        layout.addStretch()
        return widget
    
    def create_greek_tab(self):
        """ギリシャ文字タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 小文字
        lowercase_group = QGroupBox("小文字")
        lowercase_layout = QGridLayout()
        
        lowercase = [
            ("α", r"\alpha"), ("β", r"\beta"), ("γ", r"\gamma"), ("δ", r"\delta"),
            ("ε", r"\epsilon"), ("ζ", r"\zeta"), ("η", r"\eta"), ("θ", r"\theta"),
            ("ι", r"\iota"), ("κ", r"\kappa"), ("λ", r"\lambda"), ("μ", r"\mu"),
            ("ν", r"\nu"), ("ξ", r"\xi"), ("ο", r"o"), ("π", r"\pi"),
            ("ρ", r"\rho"), ("σ", r"\sigma"), ("τ", r"\tau"), ("υ", r"\upsilon"),
            ("φ", r"\phi"), ("χ", r"\chi"), ("ψ", r"\psi"), ("ω", r"\omega"),
        ]
        
        row, col = 0, 0
        for label, latex in lowercase:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            lowercase_layout.addWidget(btn, row, col)
            col += 1
            if col > 5:
                col = 0
                row += 1
        
        lowercase_group.setLayout(lowercase_layout)
        layout.addWidget(lowercase_group)
        
        # 大文字
        uppercase_group = QGroupBox("大文字")
        uppercase_layout = QGridLayout()
        
        uppercase = [
            ("Γ", r"\Gamma"), ("Δ", r"\Delta"), ("Θ", r"\Theta"), ("Λ", r"\Lambda"),
            ("Ξ", r"\Xi"), ("Π", r"\Pi"), ("Σ", r"\Sigma"), ("Φ", r"\Phi"),
            ("Ψ", r"\Psi"), ("Ω", r"\Omega"),
        ]
        
        row, col = 0, 0
        for label, latex in uppercase:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            uppercase_layout.addWidget(btn, row, col)
            col += 1
            if col > 5:
                col = 0
                row += 1
        
        uppercase_group.setLayout(uppercase_layout)
        layout.addWidget(uppercase_group)
        
        layout.addStretch()
        return widget
    
    def create_functions_tab(self):
        """関数タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 三角関数
        trig_group = QGroupBox("三角関数")
        trig_layout = QGridLayout()
        
        trig = [
            ("sin", r"\sin"), ("cos", r"\cos"), ("tan", r"\tan"),
            ("csc", r"\csc"), ("sec", r"\sec"), ("cot", r"\cot"),
            ("arcsin", r"\arcsin"), ("arccos", r"\arccos"), ("arctan", r"\arctan"),
            ("sinh", r"\sinh"), ("cosh", r"\cosh"), ("tanh", r"\tanh"),
        ]
        
        row, col = 0, 0
        for label, latex in trig:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            trig_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        trig_group.setLayout(trig_layout)
        layout.addWidget(trig_group)
        
        # 対数・指数
        log_group = QGroupBox("対数・指数")
        log_layout = QGridLayout()
        
        log = [
            ("log", r"\log"), ("ln", r"\ln"), ("exp", r"\exp"),
            ("log₁₀", r"\log_{10}"), ("logₐ", r"\log_{a}"),
        ]
        
        row, col = 0, 0
        for label, latex in log:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            log_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        layout.addStretch()
        return widget
    
    def create_misc_tab(self):
        """その他タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 矢印
        arrow_group = QGroupBox("矢印")
        arrow_layout = QGridLayout()
        
        arrows = [
            ("→", r"\to"), ("←", r"\leftarrow"), ("↔", r"\leftrightarrow"),
            ("⇒", r"\Rightarrow"), ("⇐", r"\Leftarrow"), ("⇔", r"\Leftrightarrow"),
            ("↑", r"\uparrow"), ("↓", r"\downarrow"), ("⇑", r"\Uparrow"), ("⇓", r"\Downarrow"),
        ]
        
        row, col = 0, 0
        for label, latex in arrows:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            arrow_layout.addWidget(btn, row, col)
            col += 1
            if col > 5:
                col = 0
                row += 1
        
        arrow_group.setLayout(arrow_layout)
        layout.addWidget(arrow_group)
        
        # 特殊記号
        special_group = QGroupBox("特殊記号")
        special_layout = QGridLayout()
        
        special = [
            ("∞", r"\infty"), ("∂", r"\partial"), ("∇", r"\nabla"),
            ("±", r"\pm"), ("∓", r"\mp"), ("×", r"\times"), ("÷", r"\div"),
            ("・", r"\cdot"), ("…", r"\cdots"), ("⋮", r"\vdots"), ("⋱", r"\ddots"),
            ("∅", r"\emptyset"), ("ℝ", r"\mathbb{R}"), ("ℂ", r"\mathbb{C}"),
            ("ℕ", r"\mathbb{N}"), ("ℤ", r"\mathbb{Z}"), ("ℚ", r"\mathbb{Q}"),
        ]
        
        row, col = 0, 0
        for label, latex in special:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, l=latex: self.insert_latex(l))
            special_layout.addWidget(btn, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        special_group.setLayout(special_layout)
        layout.addWidget(special_group)
        
        layout.addStretch()
        return widget
    
    def insert_latex(self, latex_code):
        """LaTeXコードを挿入"""
        cursor = self.latex_edit.textCursor()
        cursor.insertText(latex_code)
        self.latex_edit.setFocus()
    
    def on_mode_changed(self):
        """モード変更時"""
        if self.inline_radio.isChecked():
            self.current_mode = "inline"
        else:
            self.current_mode = "display"
        self.update_preview()
    
    def update_preview(self):
        """プレビューを更新"""
        latex = self.latex_edit.toPlainText().strip()
        
        if not latex:
            latex = r"\text{ここに数式が表示されます}"
        
        # モードに応じて数式を囲む
        if self.current_mode == "inline":
            display_latex = f"${latex}$"
        else:
            display_latex = f"$${latex}$$"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js"></script>
            <script>
                MathJax = {{
                    tex: {{
                        inlineMath: [['$', '$']],
                        displayMath: [['$$', '$$']],
                        processEscapes: true
                    }},
                    startup: {{
                        pageReady: () => {{
                            return MathJax.startup.defaultPageReady().then(() => {{
                                console.log('MathJax ready');
                            }});
                        }}
                    }}
                }};
            </script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 18pt;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100px;
                }}
                .math-display {{
                    text-align: center;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="math-display">{display_latex}</div>
        </body>
        </html>
        """
        
        self.preview_view.setHtml(html)
    
    def clear_formula(self):
        """数式をクリア"""
        self.latex_edit.clear()
    
    def accept_formula(self):
        """数式を確定"""
        self.current_formula = self.latex_edit.toPlainText().strip()
        
        if not self.current_formula:
            return
        
        # シグナルを発行
        self.formula_accepted.emit(self.current_formula, self.current_mode)
        self.accept()
    
    def get_formula(self):
        """入力された数式を取得"""
        return self.current_formula
    
    def get_mode(self):
        """選択されたモードを取得"""
        return self.current_mode
