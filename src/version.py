# -*- coding: utf-8 -*-
"""バージョン情報管理"""

from pathlib import Path

__version__ = "1.2.0"
__version_info__ = (1, 2, 0)

# リリースノート
RELEASE_NOTES = {
    "1.2.0": [
        "外部スクリプト実行のタイムアウト撤廃（無制限実行可能）",
        "3つすべての外部スクリプトがツールバーに表示されるように修正",
        "スクリプトメニューのクロージャ問題を修正",
        "長時間実行スクリプトに対応",
    ],
    "1.1.0": [
        "問題に配点フィールドを追加",
        "HTMLエクスポートのレイアウト改善（日本語問題番号、配点表示）",
        "表紙データのJSON保存/読み込み修正",
        "数式表示のスタイル改善",
        "必答・選択の区別機能（実装予定）",
        "解答欄自動生成機能（実装予定）",
        "PDF直接出力機能（実装予定）",
        "問題並び替え機能（実装予定）",
        "画像挿入機能（実装予定）",
    ],
    "1.0.0": [
        "初回リリース",
        "プロジェクト管理（新規作成、開く、保存）",
        "表紙編集機能",
        "マークダウン問題エディタ",
        "HTML問題エディタ",
        "HTML出力機能",
        "プロンプト生成機能",
    ]
}


def get_version() -> str:
    """バージョン文字列を取得"""
    return __version__


def get_version_info() -> tuple:
    """バージョン情報タプルを取得"""
    return __version_info__


def get_release_notes(version: str = None) -> list:
    """特定バージョンのリリースノートを取得
    
    Args:
        version: バージョン文字列（Noneの場合は最新版）
    
    Returns:
        リリースノートのリスト
    """
    if version is None:
        version = __version__
    return RELEASE_NOTES.get(version, [])


def get_all_versions() -> list:
    """すべてのバージョンを取得（新しい順）"""
    versions = list(RELEASE_NOTES.keys())
    versions.sort(key=lambda v: [int(x) for x in v.split('.')], reverse=True)
    return versions
