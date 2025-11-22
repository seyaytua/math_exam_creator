#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テストスクリプト1: 基本動作確認
"""

import sys
import datetime

def main():
    print("=" * 60)
    print("Math Exam Creator - 外部スクリプトテスト")
    print("=" * 60)
    print()
    
    print(f"実行時刻: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Pythonバージョン: {sys.version}")
    print(f"スクリプトパス: {__file__}")
    print()
    
    print("✓ スクリプトが正常に実行されました")
    print()
    
    # 簡単な計算例
    print("数学の計算例:")
    print(f"  2 + 3 = {2 + 3}")
    print(f"  10 * 5 = {10 * 5}")
    print(f"  √16 = {16 ** 0.5}")
    print()
    
    print("=" * 60)
    print("実行完了")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
