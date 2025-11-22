@echo off
REM Windows用ビルドスクリプト

echo =========================================
echo Math Exam Creator - Windows Build Script
echo =========================================
echo.

REM Python環境チェック
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python が見つかりません
    pause
    exit /b 1
)

python --version
echo.

REM 仮想環境の作成（推奨）
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM 仮想環境の有効化
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM 依存パッケージのインストール
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM xhtml2pdfのインストール（PDF出力用）
echo.
echo Installing xhtml2pdf for PDF support...
pip install xhtml2pdf

REM ビルド
echo.
echo Building application...
pyinstaller build.spec --clean

REM 結果の確認
if exist "dist\MathExamCreator" (
    echo.
    echo =========================================
    echo Build successful!
    echo =========================================
    echo.
    echo Application: dist\MathExamCreator
    echo.
    echo To create an installer, use Inno Setup:
    echo   https://jrsoftware.org/isinfo.php
    echo.
) else (
    echo.
    echo =========================================
    echo Build failed
    echo =========================================
    pause
    exit /b 1
)

pause
