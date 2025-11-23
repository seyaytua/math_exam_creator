# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for Math Exam Creator
"""

import sys
from pathlib import Path

block_cipher = None

# アプリケーション名
app_name = 'Math Exam Creator'

# データファイル
datas = [
    ('src', 'src'),
    ('VERSION', '.'),
]

# リソースファイルがある場合
resources_dir = Path('resources')
if resources_dir.exists():
    datas.append(('resources', 'resources'))

# 隠しインポート
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebEngineCore',
    'PySide6.QtPrintSupport',  # 印刷機能用
    'markdown',
    'markdown.extensions',
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.fenced_code',
    'pymdownx',
    'pymdownx.superfences',
    'pymdownx.arithmatex',
    # WeasyPrint関連
    'weasyprint',
    'weasyprint.css',
    'weasyprint.css.counters',
    'weasyprint.css.media_queries',
    'weasyprint.css.style_for',
    'weasyprint.css.targets',
    'weasyprint.html',
    'weasyprint.layout',
    'weasyprint.pdf',
    'weasyprint.text',
    'cairocffi',
    'cairosvg',
    'cffi',
    'cssselect2',
    'tinycss2',
    'pyphen',
    'fonttools',
    'fonttools.ttLib',
]

# WeasyPrintのバイナリとデータを収集
binaries = []
weasyprint_datas = []

try:
    import weasyprint
    import cairocffi
    import pyphen
    
    # Pyphenの辞書データを追加
    pyphen_path = Path(pyphen.__file__).parent
    if (pyphen_path / 'dictionaries').exists():
        weasyprint_datas.append((str(pyphen_path / 'dictionaries'), 'pyphen/dictionaries'))
except ImportError:
    pass

# プラットフォーム別の設定
if sys.platform == 'darwin':
    # macOS
    try:
        # Cairoライブラリのパスを追加
        import cairocffi
        cairo_lib_path = cairocffi.__path__[0]
        # macOSのCairoバイナリを探す
        for lib_path in ['/opt/homebrew/lib', '/usr/local/lib']:
            lib_path = Path(lib_path)
            if lib_path.exists():
                for lib_file in ['libcairo.2.dylib', 'libpango-1.0.dylib', 'libpangocairo-1.0.dylib']:
                    full_path = lib_path / lib_file
                    if full_path.exists():
                        binaries.append((str(full_path), '.'))
    except:
        pass
    
    icon_file = 'resources/icon.icns' if Path('resources/icon.icns').exists() else None

elif sys.platform == 'win32':
    # Windows
    # WindowsではGTK+ランタイムが必要
    # GTK3-Runtime for Windows をインストールする必要がある
    icon_file = 'resources/icon.ico' if Path('resources/icon.ico').exists() else None
    
else:
    # Linux
    icon_file = None

# データファイルにweasyprintのデータを追加
datas.extend(weasyprint_datas)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name if sys.platform == 'darwin' else 'MathExamCreator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUIアプリケーションなのでコンソールを非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name if sys.platform == 'darwin' else 'MathExamCreator',
)

# macOS用のappバンドル作成
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=f'{app_name}.app',
        icon=icon_file,
        bundle_identifier='com.mathexamcreator.app',
        info_plist={
            'CFBundleName': app_name,
            'CFBundleDisplayName': app_name,
            'CFBundleVersion': '1.4.0',
            'CFBundleShortVersionString': '1.4.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.15.0',
        },
    )
