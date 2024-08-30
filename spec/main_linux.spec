# main_linux.spec
# -*- mode: python ; coding: utf-8 -*-

import shutil
import os

block_cipher = None

a = Analysis(['../main.py'],
             pathex=['../', '/..env/bin'],  # Add venv path here
             binaries=[],
             datas=[
                ('../data/bin/*', 'data/bin'),
                ('../data/db/*', 'data/db'),
                ('../data/logs/*', 'data/logs'),
                ('../data/csv/*', 'data/csv'),
                ('../ICO/*', 'ICO'),
                ('../STYLE/*', 'STYLE')
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
          name='sistema_isola',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          windowed=True,  # Enable windowed mode for GUI applications
          console=False,
          icon='../ICO/logo_app.png')  # Path to your icon file

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='sistema_isola')

# Post-processing to create the .desktop file
def create_desktop_file():
    desktop_entry_content = f"""
[Desktop Entry]
Version=1.0
Name=Sistema Isola
Comment=programma sistema isola NANOLEVER
Exec={os.path.abspath('dist/sistema_isola/sistema_isola')}
Icon={os.path.abspath('dist/sistema_isola/logo_app.png')}
Terminal=false
Type=Application
Categories=Utility;Application;
    """
    # Path to the desktop file in the user's application directory
    desktop_file_path = os.path.expanduser('sistema_isola.desktop')
    with open(desktop_file_path, 'w') as desktop_file:
        desktop_file.write(desktop_entry_content)
    # Set executable permission to the .desktop file
    os.chmod(desktop_file_path, 0o755)

# Execute the function to create the .desktop file
create_desktop_file()