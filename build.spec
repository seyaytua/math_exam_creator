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
    'markdown',
    'markdown.extensions',
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.fenced_code',
    'pymdownx',
    'pymdownx.superfences',
    'pymdownx.arithmatex',
]

# プラットフォーム別の設定
if sys.platform == 'darwin':
    # macOS
    hiddenimports.extend([
        'weasyprint',
        'cairocffi',
        'cairosvg',
    ])
    icon_file = 'resources/icon.icns' if Path('resources/icon.icns').exists() else None
elif sys.platform == 'win32':
    # Windows
    hiddenimports.extend([
        'xhtml2pdf',
    ])
    icon_file = 'resources/icon.ico' if Path('resources/icon.ico').exists() else None
else:
    # Linux
    hiddenimports.extend([
        'weasyprint',
    ])
    icon_file = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
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
            'CFBundleVersion': '1.2.0',
            'CFBundleShortVersionString': '1.2.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.15.0',
        },
    )
