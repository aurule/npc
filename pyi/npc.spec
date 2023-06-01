# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


cli_analysis = Analysis(
    ['cli_entrypoint.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("../src/npc/settings/settings.yaml",       "npc/settings"),
        ("../src/npc/settings/systems/*.yaml",      "npc/settings/systems"),
        ("../src/npc/settings/types/dnd3",          "npc/settings/types/dnd3"),
        ("../src/npc/settings/types/fate",          "npc/settings/types/fate"),
        ("../src/npc/settings/types/fate-ep",       "npc/settings/types/fate-ep"),
        ("../src/npc/settings/types/fate-venture",  "npc/settings/types/fate-venture"),
        ("../src/npc/settings/types/generic",       "npc/settings/types/generic"),
        ("../src/npc/settings/types/nwod",          "npc/settings/types/nwod"),
        ("../src/npc/settings/types/wod",           "npc/settings/types/wod"),
        ("../src/npc/templates",                    "npc/templates"),
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
cli_pyz = PYZ(cli_analysis.pure, cli_analysis.zipped_data, cipher=block_cipher)

cli_exe = EXE(
    cli_pyz,
    cli_analysis.scripts,
    [],
    exclude_binaries=True,
    name='npc_cli',
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
    cli_exe,
    cli_analysis.binaries,
    cli_analysis.zipfiles,
    cli_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='npc_bin',
)
