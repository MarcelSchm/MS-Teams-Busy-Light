# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Repository\\MS-Teams-Busy-Light\\src\\MS_Teams_Busy_Light.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
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
    name='MS_Teams_Busy_Light',
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
    version='C:\\Repository\\MS-Teams-Busy-Light\\TeamsVersionFile.txt',
    icon=['C:\\Repository\\MS-Teams-Busy-Light\\images\\traffic_light.ico'],
)
