# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'..\main.py'],
    pathex=[r'..'],
    binaries=[],
    datas=[
        (r'..\data\bin\*', r'data\bin'),
        (r'..\data\db\*', r'data\db'),
        (r'..\data\testi_mail\*', r'data\testi_mail'),
        (r'..\ico\*', r'ico'),
        (r'..\risorse\resources.qrc', r'risorse\resources.qrc'),
        (r'..\risorse\resources_rc.py', r'riosrse\resources_rc.py')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='response_analyze',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Disable console
    windowed=True,  # Enable windowed mode
    onefile=True,   # Create a single executable file
    icon=r'\ico\logo_def.ico'  # Ensure you have an icon file in this path (use .ico for Windows)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='response_analyze'
)