# Resources Directory

このディレクトリには、アプリケーションのリソースファイルを配置します。

## 必要なファイル

### アイコンファイル

アプリケーションのビルドには、以下のアイコンファイルが必要です：

- **icon.icns** - macOS用アイコン（512x512px以上推奨）
- **icon.ico** - Windows用アイコン（複数サイズ含む: 16x16, 32x32, 48x48, 256x256）

### アイコンの作成方法

#### macOS用 (.icns)

```bash
# PNGファイルから.icnsを作成
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
```

#### Windows用 (.ico)

```bash
# ImageMagickを使用
convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico

# または、オンラインツールを使用
# https://convertio.co/ja/png-ico/
```

## 現在の状態

アイコンファイルがまだ作成されていない場合、PyInstallerはデフォルトのアイコンを使用します。
プロダクション用のビルドを作成する前に、カスタムアイコンを追加してください。
