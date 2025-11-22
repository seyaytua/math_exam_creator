# GitHub Actions ワークフローの設定方法

GitHub Actionsで自動ビルドを設定するための手順です。

## なぜ手動設定が必要か

GitHub Appの権限制限により、ワークフローファイル（`.github/workflows/`）を直接プッシュできません。
そのため、GitHub Web UIから手動で追加する必要があります。

## 設定手順

### 1. GitHubリポジトリを開く

1. https://github.com/seyaytua/math_exam_creator にアクセス
2. `genspark_ai_developer` ブランチに切り替え

### 2. ワークフローファイルを作成

1. リポジトリのルートで「Add file」→「Create new file」をクリック
2. ファイル名を入力: `.github/workflows/build-release.yml`
3. 以下の内容をコピー＆ペースト

### 3. ワークフローファイルの内容

```yaml
name: Build Release Executables

on:
  push:
    tags:
      - 'v*'  # v1.0.0, v1.1.0 などのタグでトリガー
  workflow_dispatch:  # 手動実行も可能

jobs:
  build-macos:
    name: Build macOS App
    runs-on: macos-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install system dependencies (macOS)
      run: |
        brew install cairo pango gdk-pixbuf libffi
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
        pip install weasyprint
    
    - name: Build macOS app with PyInstaller
      run: |
        pyinstaller build.spec --clean
    
    - name: Create ZIP archive
      run: |
        cd dist
        zip -r "Math-Exam-Creator-macOS.zip" "Math Exam Creator.app"
    
    - name: Upload macOS artifact
      uses: actions/upload-artifact@v4
      with:
        name: macos-app
        path: dist/Math-Exam-Creator-macOS.zip
        retention-days: 30

  build-windows:
    name: Build Windows Executable
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
        pip install xhtml2pdf
    
    - name: Build Windows executable with PyInstaller
      run: |
        pyinstaller build.spec --clean
    
    - name: Create ZIP archive
      run: |
        Compress-Archive -Path "dist\MathExamCreator" -DestinationPath "dist\Math-Exam-Creator-Windows.zip"
    
    - name: Upload Windows artifact
      uses: actions/upload-artifact@v4
      with:
        name: windows-exe
        path: dist/Math-Exam-Creator-Windows.zip
        retention-days: 30

  create-release:
    name: Create GitHub Release
    needs: [build-macos, build-windows]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - name: Download macOS artifact
      uses: actions/download-artifact@v4
      with:
        name: macos-app
        path: ./artifacts
    
    - name: Download Windows artifact
      uses: actions/download-artifact@v4
      with:
        name: windows-exe
        path: ./artifacts
    
    - name: Create Release
      uses: softprops/action-gh-release@v2
      with:
        files: |
          ./artifacts/Math-Exam-Creator-macOS.zip
          ./artifacts/Math-Exam-Creator-Windows.zip
        draft: false
        prerelease: false
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 4. コミット

1. 下部の「Commit new file」をクリック
2. Commit message: `ci: add GitHub Actions workflow for building executables`
3. 「Commit directly to the genspark_ai_developer branch」を選択
4. 「Commit new file」をクリック

## 使い方

### 自動ビルド（タグプッシュ）

```bash
# バージョンタグを作成
git tag v1.1.0

# タグをプッシュ
git push origin v1.1.0
```

GitHub Actionsが自動的に実行され、macOSとWindows用のビルドが作成されます。
完了後、GitHub Releaseが自動作成されます。

### 手動ビルド

1. GitHubリポジトリの「Actions」タブを開く
2. 「Build Release Executables」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. ブランチを選択（通常は `genspark_ai_developer`）
5. 「Run workflow」をクリック

ビルド完了後、「Artifacts」セクションからZIPファイルをダウンロードできます。

## トラブルシューティング

### ワークフローが実行されない

- リポジトリの「Settings」→「Actions」→「General」で、
  「Allow all actions and reusable workflows」が有効になっているか確認

### ビルドが失敗する

- 「Actions」タブからワークフロー実行結果を確認
- エラーログを確認して、不足している依存関係がないかチェック

### Releaseが作成されない

- タグが `v` で始まっているか確認（例: `v1.0.0`）
- `create-release` ジョブが実行されているか確認

## 参考情報

- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [PyInstaller ドキュメント](https://pyinstaller.org/en/stable/)
- [BUILD.md](BUILD.md) - ローカルビルド手順
