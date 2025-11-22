"""プロンプト生成ダイアログ"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QCheckBox, QSpinBox, QPushButton,
    QGroupBox, QLabel, QComboBox, QTextEdit,
    QMessageBox, QApplication, QRadioButton
)
from PySide6.QtCore import Qt


class PromptGeneratorDialog(QDialog):
    """プロンプト生成ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI問題生成プロンプト")
        self.setMinimumSize(700, 800)
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        intro_label = QLabel(
            "このツールは、AIに数学の問題を作成させるためのプロンプトを生成します。\n"
            "生成されたプロンプトをClaude/ChatGPTにコピーして使用してください。"
        )
        intro_label.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 5px;")
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)
        
        # 出力形式選択グループを追加
        output_group = QGroupBox("出力形式")
        output_layout = QHBoxLayout()
        
        self.markdown_radio = QRadioButton("Markdown形式")
        self.markdown_radio.setChecked(True)
        output_layout.addWidget(self.markdown_radio)
        
        self.html_radio = QRadioButton("HTML形式")
        output_layout.addWidget(self.html_radio)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        problem_group = QGroupBox("問題設定")
        problem_layout = QFormLayout()
        
        self.topic_edit = QLineEdit()
        self.topic_edit.setPlaceholderText("例: 二次関数、三角関数、確率、微分積分")
        problem_layout.addRow("単元・トピック:", self.topic_edit)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems([
            "基礎（教科書レベル）",
            "標準（定期テストレベル）",
            "応用（入試基礎レベル）",
            "発展（入試応用レベル）"
        ])
        self.difficulty_combo.setCurrentIndex(1)
        problem_layout.addRow("難易度:", self.difficulty_combo)
        
        self.grade_combo = QComboBox()
        self.grade_combo.addItems([
            "中学1年", "中学2年", "中学3年",
            "高校1年", "高校2年", "高校3年"
        ])
        self.grade_combo.setCurrentIndex(3)
        problem_layout.addRow("対象学年:", self.grade_combo)
        
        self.problem_count_spin = QSpinBox()
        self.problem_count_spin.setRange(1, 10)
        self.problem_count_spin.setValue(1)
        self.problem_count_spin.setSuffix(" 問")
        problem_layout.addRow("問題数:", self.problem_count_spin)
        
        problem_group.setLayout(problem_layout)
        layout.addWidget(problem_group)
        
        format_group = QGroupBox("問題形式")
        format_layout = QVBoxLayout()
        
        self.calc_check = QCheckBox("計算問題")
        self.calc_check.setChecked(True)
        format_layout.addWidget(self.calc_check)
        
        self.proof_check = QCheckBox("証明問題")
        format_layout.addWidget(self.proof_check)
        
        self.graph_check = QCheckBox("グラフ・図形問題")
        format_layout.addWidget(self.graph_check)
        
        self.word_check = QCheckBox("文章題")
        format_layout.addWidget(self.word_check)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        requirements_group = QGroupBox("追加要件（オプション）")
        requirements_layout = QVBoxLayout()
        
        self.additional_edit = QTextEdit()
        self.additional_edit.setPlaceholderText(
            "追加の要件があれば記入してください。\n\n"
            "例:\n"
            "- 小問を3つ含めてください\n"
            "- 実生活に関連する問題にしてください\n"
            "- 解答・解説も含めてください"
        )
        self.additional_edit.setMaximumHeight(100)
        requirements_layout.addWidget(self.additional_edit)
        
        requirements_group.setLayout(requirements_layout)
        layout.addWidget(requirements_group)
        
        generate_button = QPushButton("プロンプトを生成")
        generate_button.clicked.connect(self.generate_prompt)
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 10px;
                font-size: 14pt;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(generate_button)
        
        prompt_label = QLabel("生成されたプロンプト:")
        prompt_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(prompt_label)
        
        self.prompt_display = QTextEdit()
        self.prompt_display.setReadOnly(True)
        self.prompt_display.setPlaceholderText("「プロンプトを生成」ボタンを押すと、ここにプロンプトが表示されます")
        layout.addWidget(self.prompt_display)
        
        button_layout = QHBoxLayout()
        
        copy_button = QPushButton("クリップボードにコピー")
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        button_layout.addWidget(copy_button)
        
        button_layout.addStretch()
        
        close_button = QPushButton("閉じる")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def generate_prompt(self):
        """プロンプトを生成"""
        topic = self.topic_edit.text() or "数学"
        difficulty = self.difficulty_combo.currentText()
        grade = self.grade_combo.currentText()
        count = self.problem_count_spin.value()
        
        formats = []
        if self.calc_check.isChecked():
            formats.append("計算問題")
        if self.proof_check.isChecked():
            formats.append("証明問題")
        if self.graph_check.isChecked():
            formats.append("グラフ・図形問題")
        if self.word_check.isChecked():
            formats.append("文章題")
        
        format_text = "、".join(formats) if formats else "任意の形式"
        additional = self.additional_edit.toPlainText().strip()
        
        # HTML形式かMarkdown形式かで分岐
        if self.html_radio.isChecked():
            prompt = self._generate_html_prompt(topic, grade, difficulty, count, format_text, additional)
        else:
            prompt = self._generate_markdown_prompt(topic, grade, difficulty, count, format_text, additional)
        
        self.prompt_display.setPlainText(prompt)
    
    def _generate_markdown_prompt(self, topic, grade, difficulty, count, format_text, additional):
        """Markdown形式のプロンプトを生成"""
        prompt = f"""# 数学問題作成依頼

以下の条件に従って、数学の問題を作成してください。

## 基本情報
- **単元・トピック**: {topic}
- **対象学年**: {grade}
- **難易度**: {difficulty}
- **問題数**: {count}問
- **問題形式**: {format_text}

## 重要な出力形式の指示

**必ず以下のマークダウン形式で、コードブロック内に出力してください。**

出力は必ず ```markdown で囲んでください。

## 数式の記述ルール（重要）

### インライン数式（文中の数式）
- `$x^2$` のように、ドル記号1つで囲む
- 例: 方程式 $x^2 + 2x + 1 = 0$ を解け。

### ディスプレイ数式（独立した数式）
- `$$x^2 + y^2 = 1$$` のように、ドル記号2つで囲む
- 前後に空行を入れる

### 複数行の数式
インライン数式を使用してください：

```markdown
$t = \\cos x$ とおくと、$\\sin x \\, dx = -dt$ となる。

よって、


$$\\int \\sin x \\, dx = -dt$$
LaTeX記法
分数: \frac{{分子}}{{分母}}
根号: \sqrt{{中身}}
積分: \int
総和: \sum
上付き: x^{{2}}
下付き: x_{{i}}
注意事項
必ずコードブロック（```markdown）で囲んで出力してください

数式は基本的にインライン数式（
.
.
.
...）を使用してください

問題は明確で、曖昧さがないようにしてください

解答と解説を含めてください

適切な難易度になるよう配慮してください"""

        if additional:
            prompt += f"\n\n## 追加要件\n{additional}"

        prompt += "\n\nそれでは、**必ずマークダウンのコードブロック内に**問題を作成してください。"
        
        return prompt

    def _generate_html_prompt(self, topic, grade, difficulty, count, format_text, additional):
        """HTML形式のプロンプトを生成"""
        prompt = f"""# 数学問題作成依頼（HTML形式）

以下の条件に従って、数学の問題を作成してください。

基本情報
単元・トピック: {topic}
対象学年: {grade}
難易度: {difficulty}
問題数: {count}問
問題形式: {format_text}
出力形式
必ずHTML形式で、コードブロック内に出力してください。

出力は必ず ```html で囲んでください。

出力例
Copy<p>次の方程式を解け。</p>


$$x^2 + 5x + 6 = 0$$

<p><strong>解答</strong></p>

<p>因数分解すると $(x+2)(x+3) = 0$ となるので、</p>


$$x = -2, -3$$
数式の記述ルール
インライン数式: $x^2$ のように記述
ディスプレイ数式: $$x^2 + y^2 = 1$$ のように記述（前後に空行）
HTMLタグの使用
段落: <p>...</p>
太字: <strong>...</strong>
表: <table border="1">...</table>
改行: <br>
リスト: <ul><li>...</li></ul> または <ol><li>...</li></ol>
LaTeX記法
分数: \frac{{分子}}{{分母}}
根号: \sqrt{{中身}}
積分: \int
総和: \sum
上付き: x^{{2}}
下付き: x_{{i}}
注意事項
必ずHTMLコードブロック（```html）で囲んで出力

数式は $...$ または $$...$$ で記述

問題は明確に記述

解答と解説を含める

適切なHTMLタグを使用して構造化"""

        if additional:
            prompt += f"\n\n## 追加要件\n{additional}"

        prompt += "\n\nそれでは、**必ずHTMLのコードブロック内に**問題を作成してください。"
        
        return prompt

    def copy_to_clipboard(self):
        """クリップボードにコピー"""
        text = self.prompt_display.toPlainText()
        if not text:
            QMessageBox.warning(self, "警告", "プロンプトが生成されていません。")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        QMessageBox.information(self, "コピー完了", "プロンプトをクリップボードにコピーしました。")
