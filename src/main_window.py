# -*- coding: utf-8 -*-
"""メインウィンドウ"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QMenuBar, QMenu, QToolBar,
    QMessageBox, QFileDialog, QLabel, QInputDialog, QDialog  # QDialogを追加
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QKeySequence
from pathlib import Path
import json

from .config import config
from .styles import Styles
from .widgets import ProblemEditor
from .models import Project, Problem
from .version import get_version, get_release_notes



class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self):
        super().__init__()
        self.current_project = Project()
        self.problem_editors = []
        self.init_ui()
        self.load_window_settings()
        self.update_window_title()
        # メニューとツールバーが作成された後に外部スクリプトメニューを更新
        # QTimer.singleShotで次のイベントループで実行
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self.update_external_scripts_menu)
        QTimer.singleShot(0, self.update_script_button_menu)
    
    def init_ui(self):
        """UIの初期化"""
        self.setWindowTitle("Math Exam Creator")
        self.setStyleSheet(Styles.get_main_stylesheet())
        self.create_menu_bar()
        self.create_toolbar()
        self.create_central_widget()
        self.statusBar().showMessage("準備完了")
    
    def create_menu_bar(self):
        """メニューバー作成"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル(&F)")
        
        new_action = QAction("新規プロジェクト(&N)", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("プロジェクトを開く(&O)", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存(&S)", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("名前を付けて保存(&A)", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        export_html_action = QAction("エクスポート(&E)...", self)
        export_html_action.setShortcut(QKeySequence("Ctrl+E"))
        export_html_action.triggered.connect(self.export_html)
        file_menu.addAction(export_html_action)       
        
        exit_action = QAction("終了(&X)", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 編集メニュー
        edit_menu = menubar.addMenu("編集(&E)")
        
        self.undo_action = QAction("元に戻す(&U)", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("やり直し(&R)", self)
        self.redo_action.setShortcut(QKeySequence.Redo)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("切り取り(&T)", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("コピー(&C)", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("貼り付け(&P)", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # 挿入メニュー
        insert_menu = menubar.addMenu("挿入(&I)")
        
        insert_problem = QAction("新しい問題(&P)", self)
        insert_problem.setShortcut(QKeySequence("Ctrl+Shift+N"))
        insert_problem.triggered.connect(self.add_problem_tab)
        insert_menu.addAction(insert_problem)
        
        insert_menu.addSeparator()
        
        insert_inline_math = QAction("インライン数式(&I)", self)
        insert_inline_math.setShortcut(QKeySequence("Ctrl+M"))
        insert_inline_math.triggered.connect(self.insert_inline_math)
        insert_menu.addAction(insert_inline_math)
        
        insert_display_math = QAction("ディスプレイ数式(&D)", self)
        insert_display_math.setShortcut(QKeySequence("Ctrl+Shift+M"))
        insert_display_math.triggered.connect(self.insert_display_math)
        insert_menu.addAction(insert_display_math)
        
        insert_menu.addSeparator()
        
        open_math_editor = QAction("数式エディタ(&M)", self)
        open_math_editor.triggered.connect(self.open_math_editor)
        insert_menu.addAction(open_math_editor)
        
        # 表示メニュー
        view_menu = menubar.addMenu("表示(&V)")
        
        zoom_in = QAction("拡大(&I)", self)
        zoom_in.setShortcut(QKeySequence.ZoomIn)
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("縮小(&O)", self)
        zoom_out.setShortcut(QKeySequence.ZoomOut)
        view_menu.addAction(zoom_out)
        
        zoom_reset = QAction("実際のサイズ(&R)", self)
        zoom_reset.setShortcut(QKeySequence("Ctrl+0"))
        view_menu.addAction(zoom_reset)
        
        # ツールメニュー
        tools_menu = menubar.addMenu("ツール(&T)")
        
        prompt_generator = QAction("プロンプト生成(&P)", self)
        prompt_generator.triggered.connect(self.open_prompt_generator)
        tools_menu.addAction(prompt_generator)
        
        tools_menu.addSeparator()
        
        external_scripts = QAction("外部スクリプト設定(&E)", self)
        external_scripts.triggered.connect(self.open_external_scripts_settings)
        tools_menu.addAction(external_scripts)
        
        tools_menu.addSeparator()
        
        print_settings = QAction("印刷設定(&S)", self)
        print_settings.triggered.connect(self.open_print_settings)
        tools_menu.addAction(print_settings)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ(&H)")
        
        usage_action = QAction("使い方(&U)", self)
        usage_action.triggered.connect(self.open_usage_window)
        help_menu.addAction(usage_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("Math Exam Creatorについて(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """ツールバー作成"""
        toolbar = QToolBar("メインツールバー")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        
        new_action = QAction("新規", self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)
        
        open_action = QAction("開く", self)
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)
        
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # UNDO/REDOボタン
        self.undo_toolbar_action = QAction("↶ 元に戻す", self)
        self.undo_toolbar_action.triggered.connect(self.undo)
        self.undo_toolbar_action.setEnabled(False)
        self.undo_toolbar_action.setToolTip("元に戻す (Ctrl+Z)")
        toolbar.addAction(self.undo_toolbar_action)
        
        self.redo_toolbar_action = QAction("↷ やり直し", self)
        self.redo_toolbar_action.triggered.connect(self.redo)
        self.redo_toolbar_action.setEnabled(False)
        self.redo_toolbar_action.setToolTip("やり直し (Ctrl+Y)")
        toolbar.addAction(self.redo_toolbar_action)
        
        toolbar.addSeparator()
        
        add_problem_action = QAction("新しい問題", self)
        add_problem_action.triggered.connect(self.add_problem_tab)
        toolbar.addAction(add_problem_action)
        
        toolbar.addSeparator()
        
        # 外部スクリプト実行ボタン（ドロップダウン付き）
        from PySide6.QtWidgets import QToolButton, QMenu
        
        self.script_button = QToolButton()
        self.script_button.setText("▶ スクリプト")
        self.script_button.setPopupMode(QToolButton.InstantPopup)
        self.script_button.setToolTip("登録した外部スクリプトを実行")
        
        # スクリプトメニューを作成
        self.script_menu = QMenu()
        self.script_button.setMenu(self.script_menu)
        
        # 初期メニューを構築
        self.update_script_button_menu()
        
        toolbar.addWidget(self.script_button)
        
        self.addToolBar(toolbar)
    
    def create_central_widget(self):
        """中央ウィジェット作成"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)  # タブの並び替えを有効化
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.tabBar().tabMoved.connect(self.on_tab_moved)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        self.add_cover_tab()
        self.add_problem_tab()
        
        layout.addWidget(self.tab_widget)
    
    def add_cover_tab(self):
        """表紙タブを追加"""
        from .widgets import CoverEditor
        
        self.cover_editor = CoverEditor()
        self.cover_editor.content_changed.connect(
            lambda: self.statusBar().showMessage("表紙が変更されました")
        )
        self.cover_editor.content_changed.connect(self.update_undo_redo_actions)
        self.tab_widget.addTab(self.cover_editor, "表紙")
    
    def add_problem_tab(self):
        """問題タブを追加"""
        problem_editor = ProblemEditor()
        self.problem_editors.append(problem_editor)
        
        # テキスト変更シグナルをUNDO/REDO更新に接続
        problem_editor.text_changed.connect(self.update_undo_redo_actions)
        
        problem_number = len(self.problem_editors)
        self.tab_widget.addTab(problem_editor, f"問題 {problem_number}")
        self.tab_widget.setCurrentWidget(problem_editor)
        
        # プロジェクトに問題を追加
        problem = Problem(f"問題 {problem_number}", "")
        self.current_project.add_problem(problem)
        
        self.statusBar().showMessage(f"問題 {problem_number} を追加しました")
    
    def close_tab(self, index):
        """タブを閉じる"""
        if index == 0:
            return
        
        widget = self.tab_widget.widget(index)
        if isinstance(widget, ProblemEditor):
            self.problem_editors.remove(widget)
            self.current_project.remove_problem(index - 1)
        
        self.tab_widget.removeTab(index)
        self._update_tab_titles()
    
    def on_tab_moved(self, from_index: int, to_index: int):
        """タブが移動された時の処理"""
        # 表紙タブ（index 0）は移動させない
        if from_index == 0 or to_index == 0:
            return
        
        # エディタリストを並び替え
        from_editor_index = from_index - 1
        to_editor_index = to_index - 1
        
        if 0 <= from_editor_index < len(self.problem_editors):
            editor = self.problem_editors.pop(from_editor_index)
            self.problem_editors.insert(to_editor_index, editor)
        
        # プロジェクトの問題リストも並び替え
        if 0 <= from_editor_index < len(self.current_project.problems):
            problem = self.current_project.problems.pop(from_editor_index)
            self.current_project.problems.insert(to_editor_index, problem)
        
        self._update_tab_titles()
        self.statusBar().showMessage("問題の順序を変更しました")
    
    def on_tab_changed(self, index: int):
        """タブが切り替わったときの処理"""
        self.update_undo_redo_actions()
    
    def _update_tab_titles(self):
        """タブのタイトルを更新"""
        for i, editor in enumerate(self.problem_editors):
            self.tab_widget.setTabText(i + 1, f"問題 {i + 1}")
    
    def update_window_title(self):
        """ウィンドウタイトルを更新"""
        version = get_version()
        title = f"Math Exam Creator v{version}"
        if self.current_project.file_path:
            title += f" - {self.current_project.file_path.name}"
        else:
            title += " - 新規プロジェクト"
        self.setWindowTitle(title)
    
    def new_project(self):
        """新規プロジェクト作成"""
        reply = QMessageBox.question(
            self, "新規プロジェクト",
            "現在のプロジェクトを保存しますか？",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            if not self.save_project():
                return
        
        # 新規プロジェクト作成
        self.current_project = Project()
        self.problem_editors.clear()
        
        # タブをクリア
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
        
        # 表紙と最初の問題を追加
        self.add_cover_tab()
        self.add_problem_tab()
        
        self.update_window_title()
        self.statusBar().showMessage("新規プロジェクトを作成しました")
    
    def open_project(self):
        """プロジェクトを開く"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "プロジェクトを開く",
            str(Path.home()),
            "Math Exam Project (*.mep);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            self.current_project = Project.load(Path(file_path))
            
            # タブをクリア
            while self.tab_widget.count() > 0:
                self.tab_widget.removeTab(0)
            
            self.problem_editors.clear()
            
            # 表紙を追加
            self.add_cover_tab()
            
            # 表紙データを復元
            if self.current_project.cover_content:
                # cover_content は辞書形式なのでそのまま設定
                self.cover_editor.set_cover_data(self.current_project.cover_content)
            
            # 問題を読み込み
            for i, problem in enumerate(self.current_project.problems):
                problem_editor = ProblemEditor()
                problem_editor.set_text(problem.content)
                if hasattr(problem, 'score'):
                    problem_editor.set_score(problem.score)
                if hasattr(problem, 'problem_type'):
                    problem_editor.set_problem_type(problem.problem_type)
                self.problem_editors.append(problem_editor)
                self.tab_widget.addTab(problem_editor, f"問題 {i + 1}")
            
            self.update_window_title()
            self.statusBar().showMessage(f"プロジェクトを開きました: {Path(file_path).name}")
        
        except Exception as e:
            QMessageBox.critical(
                self, "エラー",
                f"プロジェクトの読み込みに失敗しました:\n{str(e)}"
            )
    
    def save_project(self) -> bool:
        """プロジェクトを保存"""
        if self.current_project.file_path:
            return self._do_save()
        else:
            return self.save_project_as()
    
    def save_project_as(self) -> bool:
        """プロジェクトに名前を付けて保存"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "名前を付けて保存",
            str(Path.home() / "新規プロジェクト.mep"),
            "Math Exam Project (*.mep);;All Files (*)"
        )
        
        if not file_path:
            return False
        
        self.current_project.file_path = Path(file_path)
        return self._do_save()
    
    def _do_save(self) -> bool:
        """実際の保存処理"""
        try:
            # 表紙データをプロジェクトに保存
            self.current_project.cover_content = self.cover_editor.get_cover_data()
            
            # エディタの内容をプロジェクトに保存
            for i, editor in enumerate(self.problem_editors):
                if i < len(self.current_project.problems):
                    self.current_project.problems[i].content = editor.get_text()
                    self.current_project.problems[i].score = editor.get_score()
                    self.current_project.problems[i].problem_type = editor.get_problem_type()
            
            self.current_project.save(self.current_project.file_path)
            self.update_window_title()
            self.statusBar().showMessage(f"保存しました: {self.current_project.file_path.name}")
            return True
        
        except Exception as e:
            QMessageBox.critical(
                self, "エラー",
                f"保存に失敗しました:\n{str(e)}"
            )
            return False
    
    def insert_inline_math(self):
        """インライン数式を挿入"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, ProblemEditor):
            current_widget.insert_markdown("$", "$")
    
    def insert_display_math(self):
        """ディスプレイ数式を挿入"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, ProblemEditor):
            current_widget.insert_markdown("\n$$\n", "\n$$\n")
    
    def open_math_editor(self):
        """数式エディタを開く"""
        from .dialogs import MathEditorDialog
        
        # 現在のタブがProblemEditorか確認
        current_widget = self.tab_widget.currentWidget()
        if not isinstance(current_widget, ProblemEditor):
            QMessageBox.warning(
                self,
                "警告",
                "数式エディタを使用するには、問題タブを選択してください。"
            )
            return
        
        # 数式エディタダイアログを作成
        dialog = MathEditorDialog(self)
        
        # 数式が確定されたときの処理
        def on_formula_accepted(formula, mode):
            """数式が確定されたときに呼ばれる"""
            if mode == "inline":
                # インライン数式: $...$
                current_widget.insert_markdown(f"${formula}$", "")
            else:
                # ディスプレイ数式: $$...$$
                current_widget.insert_markdown(f"\n$$\n{formula}\n$$\n", "")
        
        # シグナルを接続
        dialog.formula_accepted.connect(on_formula_accepted)
        
        # ダイアログを表示
        dialog.exec()
    
    def open_prompt_generator(self):
        """プロンプト生成ツールを開く"""
        from .dialogs import PromptGeneratorDialog
        
        dialog = PromptGeneratorDialog(self)
        dialog.exec()
    
    def open_external_scripts_settings(self):
        """外部スクリプト設定を開く"""
        from .dialogs import ExternalScriptsDialog
        
        dialog = ExternalScriptsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 設定が保存されたら、外部スクリプトメニューを更新
            self.update_external_scripts_menu()
            self.update_script_button_menu()
    
    def update_external_scripts_menu(self):
        """外部スクリプトメニューを更新"""
        try:
            # ツールメニューから既存の外部スクリプト実行メニューを削除
            menubar = self.menuBar()
            if not menubar:
                return
                
            tools_menu = None
            for action in menubar.actions():
                if action.text() == "ツール(&T)":
                    tools_menu = action.menu()
                    break
            
            if not tools_menu:
                return
        except RuntimeError:
            # メニューがまだ作成されていない場合
            return
        
        # 既存の外部スクリプト実行メニューを削除
        for action in tools_menu.actions():
            if hasattr(action, 'script_data'):
                tools_menu.removeAction(action)
        
        # 設定から外部スクリプトを読み込み
        from .config import config
        scripts = []
        for i in range(3):
            script_config = config.get(f'external_scripts.script{i+1}', {})
            if script_config.get('name') and script_config.get('script_path'):
                scripts.append({
                    'number': i + 1,
                    'name': script_config.get('name'),
                    'description': script_config.get('description', ''),
                    'python_path': script_config.get('python_path'),
                    'script_path': script_config.get('script_path')
                })
        
        # 外部スクリプトメニューを追加
        if scripts:
            # プロンプト生成の後に区切り線があるので、その後に挿入
            insert_after = None
            for action in tools_menu.actions():
                if action.text() == "プロンプト生成(&P)":
                    insert_after = action
                    break
            
            # セパレータの後に外部スクリプトメニューを追加
            if insert_after:
                actions = tools_menu.actions()
                separator_index = actions.index(insert_after) + 1
                
                for script in scripts:
                    script_action = QAction(f"▶ {script['name']}", self)
                    if script['description']:
                        script_action.setToolTip(script['description'])
                    script_action.script_data = script
                    # クロージャの問題を避けるため、デフォルト引数で値を固定
                    script_action.triggered.connect(
                        lambda checked=False, s=dict(script): self.execute_external_script(s)
                    )
                    
                    # セパレータの後に挿入
                    if separator_index < len(actions):
                        tools_menu.insertAction(actions[separator_index], script_action)
                    else:
                        tools_menu.addAction(script_action)
    
    def update_script_button_menu(self):
        """ツールバーのスクリプトボタンメニューを更新"""
        try:
            if not hasattr(self, 'script_menu'):
                return
            
            if not self.script_menu:
                return
            
            # 既存のメニュー項目をクリア
            self.script_menu.clear()
        except RuntimeError:
            # メニューがまだ作成されていない場合
            return
        
        # 設定から外部スクリプトを読み込み
        from .config import config
        scripts = []
        for i in range(3):
            script_config = config.get(f'external_scripts.script{i+1}', {})
            if script_config.get('name') and script_config.get('script_path'):
                scripts.append({
                    'number': i + 1,
                    'name': script_config.get('name'),
                    'description': script_config.get('description', ''),
                    'python_path': script_config.get('python_path'),
                    'script_path': script_config.get('script_path')
                })
        
        # スクリプトが登録されている場合
        if scripts:
            for script in scripts:
                script_action = QAction(f"{script['name']}", self)
                if script['description']:
                    script_action.setToolTip(script['description'])
                # クロージャの問題を避けるため、デフォルト引数で値を固定
                script_action.triggered.connect(
                    lambda checked=False, s=dict(script): self.execute_external_script(s)
                )
                self.script_menu.addAction(script_action)
            
            self.script_menu.addSeparator()
        
        # 「スクリプト設定」メニュー項目を追加
        settings_action = QAction("スクリプト設定...", self)
        settings_action.triggered.connect(self.open_external_scripts_settings)
        self.script_menu.addAction(settings_action)
        
        # スクリプトがない場合はボタンを無効化
        if not scripts:
            # デフォルトメッセージを表示
            no_scripts_action = QAction("（スクリプト未登録）", self)
            no_scripts_action.setEnabled(False)
            self.script_menu.insertAction(settings_action, no_scripts_action)
            self.script_menu.insertSeparator(settings_action)
    
    def execute_external_script(self, script_data: dict):
        """外部スクリプトを実行
        
        Args:
            script_data: スクリプト情報の辞書
        """
        import subprocess
        from pathlib import Path
        from .dialogs import ScriptOutputDialog
        
        name = script_data['name']
        python_path = script_data['python_path']
        script_path = script_data['script_path']
        
        # バリデーション
        if not Path(script_path).exists():
            QMessageBox.warning(
                self, "エラー",
                f"スクリプトファイルが見つかりません:\n{script_path}"
            )
            return
        
        if not Path(python_path).exists():
            QMessageBox.warning(
                self, "エラー",
                f"Pythonインタープリタが見つかりません:\n{python_path}"
            )
            return
        
        # 実行確認
        reply = QMessageBox.question(
            self, "スクリプト実行",
            f"スクリプト '{name}' を実行しますか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 実行
        self.statusBar().showMessage(f"スクリプトを実行中: {name}")
        
        try:
            # プラットフォーム別の設定
            import sys
            import os
            
            startupinfo = None
            creationflags = 0
            extra_kwargs = {}
            
            if sys.platform == 'win32':
                # Windows: コンソールウィンドウを非表示
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = subprocess.CREATE_NO_WINDOW
            elif sys.platform == 'darwin':
                # macOS: 新しいターミナルウィンドウを開かない
                # stdin/stdout/stderrをキャプチャすることで、ターミナルが開かなくなる
                # さらにstart_new_session=Trueで新しいセッションを作成
                extra_kwargs['start_new_session'] = True
            
            # 環境変数をコピー
            env = os.environ.copy()
            
            result = subprocess.run(
                [python_path, script_path],
                capture_output=True,
                text=True,
                # timeout: なし - スクリプトが完了するまで待機
                cwd=Path(script_path).parent,
                startupinfo=startupinfo,
                creationflags=creationflags,
                env=env,
                stdin=subprocess.DEVNULL,  # 標準入力を無効化
                **extra_kwargs
            )
            
            # 結果を表示
            output_dialog = ScriptOutputDialog(
                name,
                result.stdout,
                result.stderr,
                result.returncode,
                self
            )
            output_dialog.exec()
            
            if result.returncode == 0:
                self.statusBar().showMessage(f"スクリプト実行完了: {name}")
            else:
                self.statusBar().showMessage(f"スクリプト実行エラー: {name} (終了コード: {result.returncode})")
        
        except Exception as e:
            QMessageBox.critical(
                self, "実行エラー",
                f"スクリプトの実行中にエラーが発生しました:\n\n{str(e)}"
            )
            self.statusBar().showMessage("スクリプト実行エラー")
    
    def open_print_settings(self):
        """印刷設定を開く"""
        from .dialogs import PrintSettingsDialog
        
        dialog = PrintSettingsDialog(self)
        dialog.print_requested.connect(self.handle_print_request)
        dialog.exec()
    
    def handle_print_request(self, settings: dict):
        """印刷リクエストを処理"""
        action = settings.get('action')
        
        if action == 'preview':
            QMessageBox.information(
                self,
                "印刷プレビュー",
                "印刷プレビュー機能は今後のバージョンで実装予定です。\n\n"
                "現在は「ファイル」→「エクスポート」からHTMLまたはPDFを出力できます。"
            )
        elif action == 'print':
            QMessageBox.information(
                self,
                "印刷",
                "印刷機能は今後のバージョンで実装予定です。\n\n"
                "現在は「ファイル」→「エクスポート」からPDFを出力して印刷してください。"
            )
    
    def undo(self):
        """元に戻す"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'undo'):
            current_widget.undo()
            self.update_undo_redo_actions()
    
    def redo(self):
        """やり直す"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'redo'):
            current_widget.redo()
            self.update_undo_redo_actions()
    
    def cut(self):
        """切り取り"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, ProblemEditor):
            current_widget.text_editor.cut()
        elif hasattr(current_widget, 'focusWidget'):
            focused = current_widget.focusWidget()
            if hasattr(focused, 'cut'):
                focused.cut()
    
    def copy(self):
        """コピー"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, ProblemEditor):
            current_widget.text_editor.copy()
        elif hasattr(current_widget, 'focusWidget'):
            focused = current_widget.focusWidget()
            if hasattr(focused, 'copy'):
                focused.copy()
    
    def paste(self):
        """貼り付け"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, ProblemEditor):
            current_widget.text_editor.paste()
        elif hasattr(current_widget, 'focusWidget'):
            focused = current_widget.focusWidget()
            if hasattr(focused, 'paste'):
                focused.paste()
    
    def update_undo_redo_actions(self):
        """UNDO/REDOアクションの有効/無効を更新"""
        current_widget = self.tab_widget.currentWidget()
        
        can_undo = False
        can_redo = False
        
        if current_widget and hasattr(current_widget, 'can_undo'):
            can_undo = current_widget.can_undo()
        if current_widget and hasattr(current_widget, 'can_redo'):
            can_redo = current_widget.can_redo()
        
        self.undo_action.setEnabled(can_undo)
        self.redo_action.setEnabled(can_redo)
        self.undo_toolbar_action.setEnabled(can_undo)
        self.redo_toolbar_action.setEnabled(can_redo)
    
    def open_usage_window(self):
        """使い方ウィンドウを開く"""
        QMessageBox.information(self, "使い方", "使い方ウィンドウは実装予定です")
    
    def show_about(self):
        """アプリケーション情報を表示"""
        from .utils import PlatformUtils
        import sys
        
        version = get_version()
        release_notes = get_release_notes(version)
        notes_html = "<ul>" + "".join([f"<li>{note}</li>" for note in release_notes[:5]]) + "</ul>"
        
        # プラットフォーム情報
        platform_name = "Windows" if PlatformUtils.is_windows() else \
                       "macOS" if PlatformUtils.is_macos() else \
                       "Linux" if PlatformUtils.is_linux() else "Unknown"
        
        QMessageBox.about(
            self,
            "Math Exam Creatorについて",
            f"<h3>Math Exam Creator</h3>"
            f"<p><b>バージョン: {version}</b></p>"
            f"<p>数学考査作成支援アプリケーション</p>"
            f"<hr>"
            f"<p><b>主な機能:</b></p>"
            f"{notes_html}"
            f"<hr>"
            f"<p style='font-size: 9pt; color: #666;'>"
            f"<b>システム情報:</b><br>"
            f"プラットフォーム: {platform_name}<br>"
            f"Python: {sys.version.split()[0]}<br>"
            f"エンコーディング: UTF-8"
            f"</p>"
        )
    
    def load_window_settings(self):
        """ウィンドウ設定を読み込み"""
        width = config.get("window.width", config.DEFAULT_WINDOW_WIDTH)
        height = config.get("window.height", config.DEFAULT_WINDOW_HEIGHT)
        self.resize(width, height)
    
    def save_window_settings(self):
        """ウィンドウ設定を保存"""
        config.set("window.width", self.width())
        config.set("window.height", self.height())
    
    def closeEvent(self, event):
        """ウィンドウを閉じる時の処理"""
        self.save_window_settings()
        event.accept()

    def export_html(self):
        """HTMLまたはPDFとしてエクスポート"""
        from .dialogs import ExportDialog
        from .exporters import HTMLExporter, PDFExporter
        
        # PDF Exporterが利用できない場合の確認
        if PDFExporter is None:
            # PDF選択時にエラーメッセージを表示
            pass  # ExportDialogで制御
        
        # エクスポート設定ダイアログを表示
        dialog = ExportDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return
        
        options = dialog.get_options()
        export_format = options.get('format', 'html')
        
        # PDFが選択されたがPDFExporterが利用できない場合
        if export_format == 'pdf' and PDFExporter is None:
            QMessageBox.warning(
                self, "PDF出力エラー",
                "PDF出力には追加のライブラリが必要です。\n\n"
                "macOSの場合、以下のコマンドを実行してください:\n\n"
                "  brew install cairo pango gdk-pixbuf libffi\n"
                "  pip3 install --upgrade weasyprint\n\n"
                "詳細はREADME.mdを参照してください。"
            )
            return
        
        # 表紙データを追加
        cover_data = self.cover_editor.get_cover_data()
        options.update(cover_data)
        
        # 保存先を選択
        if export_format == 'pdf':
            file_filter = "PDF Files (*.pdf);;All Files (*)"
            default_name = f"{self.current_project.title}.pdf"
            dialog_title = "PDFとしてエクスポート"
        else:
            file_filter = "HTML Files (*.html);;All Files (*)"
            default_name = f"{self.current_project.title}.html"
            dialog_title = "HTMLとしてエクスポート"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            dialog_title,
            str(Path.home() / default_name),
            file_filter
        )
        
        if not file_path:
            return
        
        try:
            # エディタの内容をプロジェクトに保存
            for i, editor in enumerate(self.problem_editors):
                if i < len(self.current_project.problems):
                    self.current_project.problems[i].content = editor.get_text()
                    self.current_project.problems[i].score = editor.get_score()
                    self.current_project.problems[i].problem_type = editor.get_problem_type()
            
            # 表紙データをプロジェクトに保存（JSON形式）
            self.current_project.cover_content = json.dumps(cover_data, ensure_ascii=False)
            
            # エクスポート
            if export_format == 'pdf':
                exporter = PDFExporter()
                exporter.export(self.current_project, Path(file_path), options)
                self.statusBar().showMessage(f"PDFファイルを出力しました: {Path(file_path).name}")
                
                # 確認ダイアログ
                reply = QMessageBox.question(
                    self, "エクスポート完了",
                    "PDFファイルを出力しました。\n開きますか？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    import webbrowser
                    webbrowser.open(str(file_path))
            else:
                exporter = HTMLExporter()
                exporter.export(self.current_project, Path(file_path), options)
                self.statusBar().showMessage(f"HTMLファイルを出力しました: {Path(file_path).name}")
                
                # 確認ダイアログ
                reply = QMessageBox.question(
                    self, "エクスポート完了",
                    "HTMLファイルを出力しました。\n開きますか？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    import webbrowser
                    webbrowser.open(file_path)
        
        except ImportError as e:
            QMessageBox.warning(
                self, "PDF出力エラー",
                f"PDF出力には追加のライブラリが必要です:\n\n{str(e)}\n\n"
                "以下のコマンドでインストールしてください:\n"
                "  pip install weasyprint\n"
                "または\n"
                "  pip install xhtml2pdf"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "エラー",
                f"エクスポートに失敗しました:\n{str(e)}"
            )