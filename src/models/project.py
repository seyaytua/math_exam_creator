# -*- coding: utf-8 -*-
"""プロジェクトデータモデル"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys

# プラットフォーム互換性のための設定
if sys.platform.startswith('win'):
    # Windowsの場合は改行コードを統一
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'


class Problem:
    """問題データクラス"""
    
    def __init__(self, title: str = "", content: str = "", score: str = "", 
                 problem_type: str = "required"):
        self.title = title
        self.content = content
        self.score = score  # 配点（例: "15", "20点"）
        self.problem_type = problem_type  # "required" (必答) or "optional" (選択)
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書に変換"""
        return {
            "title": self.title,
            "content": self.content,
            "score": self.score,
            "problem_type": self.problem_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Problem':
        """辞書から生成"""
        problem = cls(
            data.get("title", ""), 
            data.get("content", ""),
            data.get("score", ""),
            data.get("problem_type", "required")
        )
        problem.created_at = data.get("created_at", datetime.now().isoformat())
        problem.updated_at = data.get("updated_at", datetime.now().isoformat())
        return problem


class Project:
    """プロジェクトクラス"""
    
    def __init__(self):
        self.title = "新規プロジェクト"
        self.cover_content = ""
        self.problems: List[Problem] = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.file_path: Optional[Path] = None
    
    def add_problem(self, problem: Problem):
        """問題を追加"""
        self.problems.append(problem)
        self.updated_at = datetime.now().isoformat()
    
    def remove_problem(self, index: int):
        """問題を削除"""
        if 0 <= index < len(self.problems):
            self.problems.pop(index)
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書に変換"""
        return {
            "version": "1.0",
            "title": self.title,
            "cover_content": self.cover_content,
            "problems": [p.to_dict() for p in self.problems],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """辞書から生成"""
        project = cls()
        project.title = data.get("title", "新規プロジェクト")
        project.cover_content = data.get("cover_content", "")
        project.problems = [Problem.from_dict(p) for p in data.get("problems", [])]
        project.created_at = data.get("created_at", datetime.now().isoformat())
        project.updated_at = data.get("updated_at", datetime.now().isoformat())
        return project
    
    def save(self, file_path: Path):
        """プロジェクトを保存（プラットフォーム互換）"""
        self.file_path = file_path
        self.updated_at = datetime.now().isoformat()
        
        # UTF-8で統一（Windows でも BOM なし）
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, file_path: Path) -> 'Project':
        """プロジェクトを読み込み（プラットフォーム互換）"""
        # UTF-8 で読み込み（Windows の BOM も自動処理）
        encodings = ['utf-8-sig', 'utf-8', 'cp932', 'shift-jis']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    data = json.load(f)
                
                project = cls.from_dict(data)
                project.file_path = file_path
                return project
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
        
        # すべて失敗した場合
        raise ValueError(f"プロジェクトファイルを読み込めませんでした: {file_path}")
    
    def is_modified(self) -> bool:
        """変更されているかチェック"""
        # 簡易実装：更新日時をチェック
        return True  # 後で実装
