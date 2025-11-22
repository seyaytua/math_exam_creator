# -*- coding: utf-8 -*-
"""外部スクリプト機能のテスト"""

import sys
import subprocess
from pathlib import Path

def test_external_scripts_exist():
    """テストスクリプトファイルが存在することを確認"""
    test_scripts_dir = Path(__file__).parent.parent / "test_scripts"
    
    assert test_scripts_dir.exists(), "test_scripts directory not found"
    
    test_script_1 = test_scripts_dir / "test_script_1.py"
    test_script_2 = test_scripts_dir / "test_script_2.py"
    test_script_3 = test_scripts_dir / "test_script_3_error.py"
    
    assert test_script_1.exists(), "test_script_1.py not found"
    assert test_script_2.exists(), "test_script_2.py not found"
    assert test_script_3.exists(), "test_script_3_error.py not found"

def test_script_execution_success():
    """正常なスクリプトの実行をテスト"""
    test_scripts_dir = Path(__file__).parent.parent / "test_scripts"
    test_script = test_scripts_dir / "test_script_1.py"
    
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed with code {result.returncode}"
    assert "スクリプトが正常に実行されました" in result.stdout
    assert "実行完了" in result.stdout

def test_script_execution_with_output():
    """LaTeX数式生成スクリプトの実行をテスト"""
    test_scripts_dir = Path(__file__).parent.parent / "test_scripts"
    test_script = test_scripts_dir / "test_script_2.py"
    
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed with code {result.returncode}"
    assert "LaTeX数式生成スクリプト" in result.stdout
    assert r"\frac" in result.stdout  # LaTeX formula present
    assert r"\int" in result.stdout   # Integral symbol present

def test_script_execution_error():
    """エラーハンドリングをテスト"""
    test_scripts_dir = Path(__file__).parent.parent / "test_scripts"
    test_script = test_scripts_dir / "test_script_3_error.py"
    
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # このスクリプトはエラーで終了するはず
    assert result.returncode != 0, "Script should have failed but succeeded"
    
    # 標準出力にはメッセージがあるはず
    assert "標準出力に出力しています" in result.stdout
    
    # 標準エラー出力にもメッセージがあるはず
    assert "stderr" in result.stderr or "エラー" in result.stderr

def test_external_scripts_dialog_module():
    """外部スクリプトダイアログモジュールが存在することを確認"""
    dialog_file = Path(__file__).parent.parent / "src" / "dialogs" / "external_scripts_dialog.py"
    assert dialog_file.exists(), "external_scripts_dialog.py not found"
    
    output_dialog_file = Path(__file__).parent.parent / "src" / "dialogs" / "script_output_dialog.py"
    assert output_dialog_file.exists(), "script_output_dialog.py not found"

if __name__ == "__main__":
    # Run tests manually
    print("Running external scripts tests...")
    
    try:
        test_external_scripts_exist()
        print("✓ test_external_scripts_exist passed")
    except AssertionError as e:
        print(f"✗ test_external_scripts_exist failed: {e}")
    
    try:
        test_script_execution_success()
        print("✓ test_script_execution_success passed")
    except AssertionError as e:
        print(f"✗ test_script_execution_success failed: {e}")
    
    try:
        test_script_execution_with_output()
        print("✓ test_script_execution_with_output passed")
    except AssertionError as e:
        print(f"✗ test_script_execution_with_output failed: {e}")
    
    try:
        test_script_execution_error()
        print("✓ test_script_execution_error passed")
    except AssertionError as e:
        print(f"✗ test_script_execution_error failed: {e}")
    
    try:
        test_external_scripts_dialog_module()
        print("✓ test_external_scripts_dialog_module passed")
    except AssertionError as e:
        print(f"✗ test_external_scripts_dialog_module failed: {e}")
    
    print("\nAll tests completed!")
