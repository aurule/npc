# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['cli_entrypoint.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("../src/npc/settings/settings.yaml", "npc/settings"),
        ("../src/npc/settings/systems/*.yaml", "npc/settings/systems"),
        ("../src/npc/settings/types/dnd3", "npc/settings/types/dnd3"),
        ("../src/npc/settings/types/fate", "npc/settings/types/fate"),
        ("../src/npc/settings/types/fate-ep", "npc/settings/types/fate-ep"),
        ("../src/npc/settings/types/generic", "npc/settings/types/generic"),
        ("../src/npc/settings/types/nwod", "npc/settings/types/nwod"),
        ("../src/npc/settings/types/wod", "npc/settings/types/wod"),
        ("../src/npc/templates", "npc/templates"),
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='npc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='npc',
)
