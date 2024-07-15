# main_linux.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['../main.py'],
             pathex=['../'],
             binaries=[],
             datas=[
                ('../data/bin/*', 'data/bin'),
                ('../data/db/*', 'data/db'),
                ('../data/testi_mail/*', 'data/testi_mail'),
                ('../ico/*', 'ico'),
                ('../risorse/resources.qrc', 'resources.qrc'),
                ('../risorse/resources_rc.py', 'resources_rc.py')
                ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
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
          windowed=True,  # Enable windowed mode
          console=False,
          icon='../ico/logo_def.png',  # Ensure you have an icon file in this path
          onefile=True)  # Disabilita console

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='response_analyze')  # Crea un unico file
