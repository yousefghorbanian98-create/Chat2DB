# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

ct_datas, ct_bins, ct_hidden = collect_all('ctranslate2')
fw_datas, fw_bins, fw_hidden = collect_all('faster_whisper')
pa_datas, pa_bins, pa_hidden = collect_all('pyannote.audio')
cv_datas, cv_bins, cv_hidden = collect_all('cv2')
mp_datas, mp_bins, mp_hidden = collect_all('mediapipe')

a = Analysis(
    ['easyclip_engine.py'],
    pathex=[],
    binaries=ct_bins + fw_bins + pa_bins + cv_bins + mp_bins,
    datas=ct_datas + fw_datas + pa_datas + cv_datas + mp_datas,
    hiddenimports=ct_hidden + fw_hidden + pa_hidden + cv_hidden + mp_hidden + ['yt_dlp', 'torch', 'torchaudio', 'cv2', 'mediapipe'],
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
