#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ターミナル非表示テスト用スクリプト
このスクリプトは実行時にターミナルウィンドウを表示しないことを確認するためのものです
"""

import sys
import time

def main():
    print("=" * 60)
    print("ターミナル非表示テスト")
    print("=" * 60)
    print()
    print("このメッセージはスクリプト出力ダイアログに表示されますが、")
    print("別のターミナルウィンドウは開きません。")
    print()
    print("処理中...", flush=True)
    
    # 少し時間をかけて実行
    for i in range(5):
        time.sleep(0.5)
        print(f"  ステップ {i+1}/5 完了", flush=True)
    
    print()
    print("✓ テスト完了")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
