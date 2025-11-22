# ビルドガイド

Math Exam Creatorの実行ファイルをビルドする方法を説明します。

## 目次

- [GitHub Actionsでの自動ビルド](#github-actionsでの自動ビルド)
- [ローカルでのビルド](#ローカルでのビルド)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Linux](#linux)

## GitHub Actionsでの自動ビルド

### リリースタグでのビルド

1. バージョンタグを作成してプッシュ：
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

2. GitHub Actionsが自動的に実行され、以下が作成されます：
   - macOS用 `.app` バンドル（ZIP圧縮）
   - Windows用 `.exe` 実行ファイル（ZIP圧縮）
   - GitHub Release（自動作成）

3. リリースページからダウンロード可能になります：
   - `Math-Exam-Creator-macOS.zip`
   - `Math-Exam-Creator-Windows.zip`

### 手動ビルド（GitHub UI）

1. GitHubリポジトリの「Actions」タブを開く
2. 「Build Release Executables」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. ブランチを選択して実行
5. ビルド完了後、Artifactsからダウンロード可能

## ローカルでのビルド

### macOS

#### 前提条件

- macOS 10.15 (Catalina) 以降
- Python 3.11以上
- Homebrew（推奨）

#### ビルド手順

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/seyaytua/math_exam_creator.git
   cd math_exam_creator
   ```

2. **ビルドスクリプトを実行**
   ```bash
   ./build_macos.sh
   ```

3. **ビルド結果**
   - アプリケーション: `dist/Math Exam Creator.app`
   - そのままダブルクリックで起動可能

4. **DMGイメージ作成（オプション）**
   ```bash
   cd dist
   hdiutil create -volname "Math Exam Creator" \
     -srcfolder "Math Exam Creator.app" \
     -ov -format UDZO MathExamCreator.dmg
   ```

#### トラブルシューティング（macOS）

**「開発元が未確認のため開けません」エラー**

初回起動時にこのエラーが出る場合：

1. アプリを右クリック → 「開く」を選択
2. 「開く」ボタンをクリック

または、ターミナルで：
```bash
xattr -cr "Math Exam Creator.app"
```

**PDF出力が使えない**

WeasyPrintの依存関係をインストール：
```bash
brew install cairo pango gdk-pixbuf libffi
pip install weasyprint
```

### Windows

#### 前提条件

- Windows 10/11
- Python 3.11以上
- Git for Windows（推奨）

#### ビルド手順

1. **リポジトリをクローン**
   ```cmd
   git clone https://github.com/seyaytua/math_exam_creator.git
   cd math_exam_creator
   ```

2. **ビルドスクリプトを実行**
   ```cmd
   build_windows.bat
   ```

3. **ビルド結果**
   - 実行ファイル: `dist\MathExamCreator\MathExamCreator.exe`
   - フォルダごと配布可能

4. **インストーラー作成（オプション）**
   
   [Inno Setup](https://jrsoftware.org/isinfo.php)を使用してインストーラーを作成できます。

#### トラブルシューティング（Windows）

**「Windowsによって保護されました」エラー**

初回起動時にこのエラーが出る場合：

1. 「詳細情報」をクリック
2. 「実行」ボタンをクリック

**PDF出力が使えない**

xhtml2pdfがインストールされていることを確認：
```cmd
pip install xhtml2pdf
```

### Linux

#### 前提条件

- Ubuntu 20.04以降（または同等のディストリビューション）
- Python 3.11以上

#### ビルド手順

1. **依存パッケージのインストール**
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
     python3-pip \
     python3-venv \
     libcairo2 \
     libpango-1.0-0 \
     libpangocairo-1.0-0 \
     libgdk-pixbuf2.0-0 \
     libffi-dev
   ```

2. **リポジトリをクローン**
   ```bash
   git clone https://github.com/seyaytua/math_exam_creator.git
   cd math_exam_creator
   ```

3. **仮想環境の作成とビルド**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pyinstaller weasyprint
   pyinstaller build.spec --clean
   ```

4. **ビルド結果**
   - 実行ファイル: `dist/MathExamCreator/MathExamCreator`

5. **AppImage作成（オプション）**
   
   [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy)を使用してAppImageを作成できます。

## カスタマイズ

### アイコンの変更

1. `resources/icon.icns`（macOS用）
2. `resources/icon.ico`（Windows用）

を作成してください。詳細は `resources/README.md` を参照。

### ビルド設定の変更

`build.spec` ファイルを編集して、以下をカスタマイズできます：

- アプリケーション名
- バンドルID（macOS）
- 含めるデータファイル
- 隠しインポート
- 除外するモジュール

### バージョン番号の更新

1. `VERSION` ファイル
2. `src/version.py` の `__version__`
3. `build.spec` の `CFBundleVersion`（macOS）

を更新してください。

## ビルドサイズの最適化

### 不要なモジュールの除外

`build.spec` の `excludes` リストに追加：
```python
excludes=[
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    # その他不要なモジュール
]
```

### UPX圧縮

PyInstallerはデフォルトでUPX圧縮を使用しますが、問題がある場合は無効化できます：
```python
upx=False
```

## CI/CDワークフロー

`.github/workflows/build-release.yml` で定義されています。

### トリガー条件

1. **タグプッシュ**: `v*` パターン（例: v1.0.0, v1.1.0）
2. **手動実行**: GitHub UIから実行可能

### ビルドプロセス

1. **macOSビルド**
   - macOS-latest runner
   - Python 3.11
   - Homebrewで依存関係をインストール
   - PyInstallerでビルド
   - ZIPで圧縮
   - Artifactとしてアップロード

2. **Windowsビルド**
   - windows-latest runner
   - Python 3.11
   - PyInstallerでビルド
   - ZIPで圧縮
   - Artifactとしてアップロード

3. **リリース作成**（タグプッシュ時のみ）
   - 両プラットフォームのビルドをダウンロード
   - GitHub Releaseを作成
   - ビルドファイルを添付
   - リリースノートを自動生成

## サポート

ビルドに関する問題は、GitHubのIssuesで報告してください。
