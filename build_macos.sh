#!/bin/bash
# macOS用ビルドスクリプト

set -e

echo "========================================="
echo "Math Exam Creator - macOS Build Script"
echo "========================================="
echo ""

# Python環境チェック
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 が見つかりません"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# 仮想環境の作成（推奨）
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 仮想環境の有効化
echo "Activating virtual environment..."
source venv/bin/activate

# 依存パッケージのインストール
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# WeasyPrintのインストール（オプション）
echo ""
read -p "Install WeasyPrint for PDF support? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing WeasyPrint..."
    brew install cairo pango gdk-pixbuf libffi 2>/dev/null || echo "Please install Homebrew dependencies manually"
    pip install weasyprint
fi

# ビルド
echo ""
echo "Building application..."
pyinstaller build.spec --clean

# 結果の確認
if [ -d "dist/Math Exam Creator.app" ]; then
    echo ""
    echo "========================================="
    echo "✓ Build successful!"
    echo "========================================="
    echo ""
    echo "Application: dist/Math Exam Creator.app"
    echo ""
    echo "To create a DMG:"
    echo "  cd dist"
    echo "  hdiutil create -volname 'Math Exam Creator' -srcfolder 'Math Exam Creator.app' -ov -format UDZO MathExamCreator.dmg"
    echo ""
else
    echo ""
    echo "========================================="
    echo "✗ Build failed"
    echo "========================================="
    exit 1
fi
