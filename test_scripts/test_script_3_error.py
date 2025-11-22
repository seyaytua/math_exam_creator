#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テストスクリプト3: エラーハンドリング確認用
このスクリプトは意図的にエラーを発生させます
"""

import sys

def main():
    print("標準出力に出力しています...")
    print("このメッセージは正常に表示されます")
    
    # 標準エラー出力にメッセージを出力
    print("警告: これはstderrへの出力です", file=sys.stderr)
    
    # 意図的にエラーを発生させる
    print("エラーを発生させます...", file=sys.stderr)
    raise ValueError("これはテスト用のエラーです")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"エラー: {str(e)}", file=sys.stderr)
        sys.exit(1)
