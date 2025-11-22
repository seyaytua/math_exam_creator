# -*- coding: utf-8 -*-
"""プラットフォーム互換性ユーティリティ"""

import sys
import os
from pathlib import Path


class PlatformUtils:
    """プラットフォーム間の互換性を保証するユーティリティ"""
    
    @staticmethod
    def is_windows() -> bool:
        """Windows環境かチェック"""
        return sys.platform.startswith('win')
    
    @staticmethod
    def is_macos() -> bool:
        """macOS環境かチェック"""
        return sys.platform == 'darwin'
    
    @staticmethod
    def is_linux() -> bool:
        """Linux環境かチェック"""
        return sys.platform.startswith('linux')
    
    @staticmethod
    def normalize_line_endings(text: str) -> str:
        """改行コードを統一（LF=\\nに統一）
        
        Args:
            text: 処理対象のテキスト
        
        Returns:
            改行コードを統一したテキスト
        """
        # Windows形式（CRLF）→ Unix形式（LF）
        text = text.replace('\r\n', '\n')
        # 古いMac形式（CR）→ Unix形式（LF）
        text = text.replace('\r', '\n')
        return text
    
    @staticmethod
    def normalize_path(path_str: str) -> Path:
        """パスを正規化してPathオブジェクトに変換
        
        Args:
            path_str: パス文字列
        
        Returns:
            正規化されたPathオブジェクト
        """
        # バックスラッシュをスラッシュに統一
        normalized = path_str.replace('\\\\', '/').replace('\\', '/')
        return Path(normalized)
    
    @staticmethod
    def get_default_encoding() -> str:
        """デフォルトの文字エンコーディングを取得
        
        Returns:
            推奨エンコーディング名
        """
        if PlatformUtils.is_windows():
            # Windowsでも UTF-8 を推奨
            return 'utf-8-sig'  # BOM付きUTF-8
        else:
            return 'utf-8'
    
    @staticmethod
    def safe_file_read(file_path: Path) -> str:
        """プラットフォームに依存しない安全なファイル読み込み
        
        Args:
            file_path: 読み込むファイルのパス
        
        Returns:
            ファイルの内容（改行コード統一済み）
        """
        # まず UTF-8 で試す
        encodings = ['utf-8', 'utf-8-sig']
        
        # Windows の場合は CP932 も試す
        if PlatformUtils.is_windows():
            encodings.extend(['cp932', 'shift-jis'])
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    return PlatformUtils.normalize_line_endings(content)
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # すべて失敗した場合はエラー
        raise ValueError(f"ファイルを読み込めませんでした: {file_path}")
    
    @staticmethod
    def safe_file_write(file_path: Path, content: str):
        """プラットフォームに依存しない安全なファイル書き込み
        
        Args:
            file_path: 書き込むファイルのパス
            content: 書き込む内容
        """
        # 改行コードを統一してから書き込み
        content = PlatformUtils.normalize_line_endings(content)
        
        encoding = PlatformUtils.get_default_encoding()
        with open(file_path, 'w', encoding=encoding, newline='\n') as f:
            f.write(content)
    
    @staticmethod
    def get_system_info() -> dict:
        """システム情報を取得
        
        Returns:
            システム情報の辞書
        """
        return {
            'platform': sys.platform,
            'is_windows': PlatformUtils.is_windows(),
            'is_macos': PlatformUtils.is_macos(),
            'is_linux': PlatformUtils.is_linux(),
            'python_version': sys.version,
            'default_encoding': sys.getdefaultencoding(),
            'filesystem_encoding': sys.getfilesystemencoding(),
            'recommended_encoding': PlatformUtils.get_default_encoding()
        }
