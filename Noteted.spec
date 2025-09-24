# -*- mode: python ; coding: utf-8 -*-

import sys

# Set the icon file based on the platform
if sys.platform == 'win32':
    icon_file = 'assets/NTD.ico'
else:
    icon_file = 'assets/NTD.png'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('gitver.txt', '.')],
    hiddenimports=['pypresence', 'tkhtmlview', 'PIL._tkinter_finder'],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Noteted',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)