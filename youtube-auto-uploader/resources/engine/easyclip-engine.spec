# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

ct_datas, ct_bins, ct_hidden = collect_all('ctranslate2')
fw_datas, fw_bins, fw_hidden = collect_all('faster_whisper')

a = Analysis(
    ['easyclip_engine.py'],
    pathex=[],
    binaries=ct_bins + fw_bins,
    datas=ct_datas + fw_datas,
    hiddenimports=ct_hidden + fw_hidden + ['yt_dlp'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='easyclip-engine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
