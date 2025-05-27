# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Собираем все необходимые данные для pygame
datas = []
binaries = []
hiddenimports = ['pygame']
tmp_ret = collect_all('pygame')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Добавляем все модули importlib
for module in collect_submodules('importlib'):
    hiddenimports.append(module)

# Добавляем часто используемые модули
hiddenimports.extend(['os', 'sys', 'traceback', 'importlib', 'importlib.util'])

# Определяем пути к ассетам и исходному коду
assets_path = os.path.join('ninja_game', 'assets')
src_path = os.path.join('ninja_game', 'src')

datas.extend([
    (assets_path, 'ninja_game/assets'),
    (src_path, 'ninja_game/src'),
    ('build_game.py', '.'),
    ('ninja_game', 'ninja_game')
])

block_cipher = None

a = Analysis(
    ['debug_launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
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
    name='NinjaGame_Launcher',
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