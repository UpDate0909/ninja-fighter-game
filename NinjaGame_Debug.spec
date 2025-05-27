# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# Собираем все необходимые данные для pygame
datas = []
binaries = []
hiddenimports = ['pygame']
tmp_ret = collect_all('pygame')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Определяем пути к ассетам
assets_path = os.path.join('ninja_game', 'assets')
assets_data = [(assets_path, 'ninja_game/assets')]

block_cipher = None

a = Analysis(
    ['build_game.py'],
    pathex=[],
    binaries=binaries,
    datas=datas + assets_data,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NinjaGame_Debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Включаем консоль для отладки
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('ninja_game', 'assets', 'icon.ico') if os.path.exists(os.path.join('ninja_game', 'assets', 'icon.ico')) else None,
) 