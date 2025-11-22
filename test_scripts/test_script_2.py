#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テストスクリプト2: LaTeX数式生成例
"""

import sys

def generate_quadratic_formula():
    """二次方程式の解の公式を生成"""
    return r"$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$"

def generate_pythagorean_theorem():
    """ピタゴラスの定理を生成"""
    return r"$$a^2 + b^2 = c^2$$"

def generate_integral_example():
    """積分の例を生成"""
    return r"$$\int_{0}^{1} x^2 dx = \left[\frac{x^3}{3}\right]_{0}^{1} = \frac{1}{3}$$"

def main():
    print("=" * 70)
    print("LaTeX数式生成スクリプト")
    print("=" * 70)
    print()
    
    print("以下の数式をMath Exam Creatorで使用できます:")
    print()
    
    print("1. 二次方程式の解の公式:")
    print(generate_quadratic_formula())
    print()
    
    print("2. ピタゴラスの定理:")
    print(generate_pythagorean_theorem())
    print()
    
    print("3. 積分の例:")
    print(generate_integral_example())
    print()
    
    print("=" * 70)
    print("これらの数式をコピーして問題エディタに貼り付けてください")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
