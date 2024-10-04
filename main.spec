# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py',
    'C:\\Users\\25924\\homework-killer\\function\\code.py',
    'C:\\Users\\25924\\homework-killer\\function\\log.py',
    'C:\\Users\\25924\\homework-killer\\function\\random_addon.py',
    'C:\\Users\\25924\\homework-killer\\function\\show.py',
    'C:\\Users\\25924\\homework-killer\\function\\update.py',
    'C:\\Users\\25924\\homework-killer\\api\\api_choose.py',
    'C:\\Users\\25924\\homework-killer\\api\\xiaoxin\\xiaoxin_api.py',
    'C:\\Users\\25924\\homework-killer\\api\\xiaoxin\\homework_main.py',
    'C:\\Users\\25924\\homework-killer\\api\\xiaoxin\\__init__.py',
    'C:\\Users\\25924\\homework-killer\\api\\fangao\\homework_main.py',
    'C:\\Users\\25924\\homework-killer\\api\\fangao\\fangao_api.py',
    'C:\\Users\\25924\\homework-killer\\api\\fangao\\__init__.py'],
     pathex=['C:\\Users\\25924\\homework-killer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='homework-killer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,  # 控制台模式
          windowed=True)  # 窗口模式
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='homework-killer')