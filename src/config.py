# -*- coding: utf-8 -*-
"""設定管理モジュール"""

import json
from pathlib import Path
from typing import Any, Optional


class Config:
    """アプリケーション設定を管理するクラス"""
    
    # デフォルト値
    DEFAULT_WINDOW_WIDTH = 1200
    DEFAULT_WINDOW_HEIGHT = 800
    DEFAULT_FONT_SIZE = 12
    DEFAULT_EDITOR_FONT = "Courier New"
    
    def __init__(self):
        """設定の初期化"""
        self.config_dir = Path.home() / ".math_exam_creator"
        self.config_file = self.config_dir / "config.json"
        self.settings = {}
        self.load()
    
    def load(self):
        """設定ファイルを読み込む（プラットフォーム互換）"""
        try:
            if self.config_file.exists():
                # UTF-8 で読み込み（BOM対応）
                encodings = ['utf-8-sig', 'utf-8']
                for encoding in encodings:
                    try:
                        with open(self.config_file, 'r', encoding=encoding) as f:
                            self.settings = json.load(f)
                        return
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue
                # 読み込み失敗時はデフォルト
                self.settings = self._get_default_settings()
            else:
                self.settings = self._get_default_settings()
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
            self.settings = self._get_default_settings()
    
    def save(self):
        """設定ファイルを保存する（プラットフォーム互換）"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            # UTF-8 で保存（改行コード統一）
            with open(self.config_file, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"設定ファイルの保存に失敗しました: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得する
        
        Args:
            key: 設定キー（ドット区切りで階層を表現）
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """設定値を設定する
        
        Args:
            key: 設定キー（ドット区切りで階層を表現）
            value: 設定値
        """
        keys = key.split('.')
        settings = self.settings
        
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        settings[keys[-1]] = value
        self.save()
    
    def _get_default_settings(self) -> dict:
        """デフォルト設定を取得する
        
        Returns:
            デフォルト設定の辞書
        """
        return {
            "window": {
                "width": self.DEFAULT_WINDOW_WIDTH,
                "height": self.DEFAULT_WINDOW_HEIGHT
            },
            "editor": {
                "font_family": self.DEFAULT_EDITOR_FONT,
                "font_size": self.DEFAULT_FONT_SIZE,
                "show_line_numbers": True,
                "word_wrap": True
            },
            "preview": {
                "auto_update": True,
                "update_delay": 500
            },
            "export": {
                "default_format": "pdf",
                "output_directory": str(Path.home() / "Documents")
            }
        }


# グローバルな設定インスタンス
config = Config()