# -*- coding: utf-8 -*-
"""Python実行環境検出ユーティリティ"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Optional


class PythonDetector:
    """Python実行環境を検出するユーティリティクラス"""
    
    @staticmethod
    def get_current_python() -> str:
        """現在実行中のPythonインタープリタのパスを取得
        
        Returns:
            Pythonインタープリタの絶対パス
        """
        return sys.executable
    
    @staticmethod
    def find_python_installations() -> List[str]:
        """システムにインストールされているPythonを検索
        
        Returns:
            見つかったPythonインタープリタのパスのリスト
        """
        python_paths = []
        
        # 現在のPythonを追加
        current = PythonDetector.get_current_python()
        if current:
            python_paths.append(current)
        
        # macOSの場合
        if sys.platform == 'darwin':
            # Homebrew Python
            homebrew_paths = [
                '/opt/homebrew/bin/python3',
                '/opt/homebrew/bin/python3.11',
                '/opt/homebrew/bin/python3.12',
                '/opt/homebrew/bin/python3.13',
                '/usr/local/bin/python3',
                '/usr/local/bin/python3.11',
                '/usr/local/bin/python3.12',
                '/usr/local/bin/python3.13',
            ]
            
            # Homebrew Cellar内のPython
            homebrew_cellar = Path('/opt/homebrew/Cellar')
            if homebrew_cellar.exists():
                for python_dir in homebrew_cellar.glob('python@3.*'):
                    for version_dir in python_dir.iterdir():
                        python_bin = version_dir / 'Frameworks' / 'Python.framework' / 'Versions' / '3.*' / 'bin' / 'python3*'
                        for py in Path('/').glob(str(python_bin)):
                            if py.is_file():
                                python_paths.append(str(py))
            
            # システムPython
            system_paths = [
                '/usr/bin/python3',
                '/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11',
                '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12',
                '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13',
            ]
            
            for path in homebrew_paths + system_paths:
                if os.path.isfile(path) and path not in python_paths:
                    python_paths.append(path)
        
        # Windowsの場合
        elif sys.platform == 'win32':
            # AppData内のPython
            appdata = os.getenv('LOCALAPPDATA')
            if appdata:
                programs = Path(appdata) / 'Programs' / 'Python'
                if programs.exists():
                    for python_dir in programs.glob('Python3*'):
                        python_exe = python_dir / 'python.exe'
                        if python_exe.exists():
                            python_paths.append(str(python_exe))
            
            # ProgramFiles内のPython
            for program_files in [os.getenv('ProgramFiles'), os.getenv('ProgramFiles(x86)')]:
                if program_files:
                    python_base = Path(program_files) / 'Python3*'
                    for python_dir in Path(program_files).glob('Python3*'):
                        python_exe = python_dir / 'python.exe'
                        if python_exe.exists() and str(python_exe) not in python_paths:
                            python_paths.append(str(python_exe))
            
            # PATH環境変数から検索
            path_env = os.getenv('PATH', '')
            for path_dir in path_env.split(os.pathsep):
                python_exe = Path(path_dir) / 'python.exe'
                if python_exe.exists() and str(python_exe) not in python_paths:
                    python_paths.append(str(python_exe))
        
        # Linuxの場合
        elif sys.platform.startswith('linux'):
            common_paths = [
                '/usr/bin/python3',
                '/usr/bin/python3.11',
                '/usr/bin/python3.12',
                '/usr/bin/python3.13',
                '/usr/local/bin/python3',
                '/usr/local/bin/python3.11',
                '/usr/local/bin/python3.12',
                '/usr/local/bin/python3.13',
            ]
            
            for path in common_paths:
                if os.path.isfile(path) and path not in python_paths:
                    python_paths.append(path)
        
        # 重複を削除
        unique_paths = []
        seen = set()
        for path in python_paths:
            # シンボリックリンクを解決
            try:
                real_path = os.path.realpath(path)
                if real_path not in seen and os.path.isfile(real_path):
                    unique_paths.append(path)
                    seen.add(real_path)
            except (OSError, ValueError):
                continue
        
        return unique_paths
    
    @staticmethod
    def get_python_version(python_path: str) -> Optional[str]:
        """Pythonのバージョンを取得
        
        Args:
            python_path: Pythonインタープリタのパス
        
        Returns:
            バージョン文字列（例: "3.11.5"）、取得できない場合はNone
        """
        try:
            result = subprocess.run(
                [python_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # "Python 3.11.5" -> "3.11.5"
                version_line = result.stdout.strip() or result.stderr.strip()
                if version_line.startswith('Python '):
                    return version_line.split(' ')[1]
            
            return None
        
        except Exception:
            return None
    
    @staticmethod
    def validate_python_path(python_path: str) -> bool:
        """Pythonパスが有効かどうかを検証
        
        Args:
            python_path: 検証するPythonインタープリタのパス
        
        Returns:
            有効な場合True、無効な場合False
        """
        if not python_path or not os.path.isfile(python_path):
            return False
        
        try:
            # 実行可能かテスト
            result = subprocess.run(
                [python_path, '-c', 'print("OK")'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return result.returncode == 0 and 'OK' in result.stdout
        
        except Exception:
            return False
