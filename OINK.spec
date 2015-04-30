# -*- mode: python -*-
a = Analysis(['.\\OINK.pyw'],
             pathex=['C:\\Users\\vinay.keerthi\\Google Drive\\Projects\\WFM\\O.I.N.K Report Management System\\Admin\\OINK'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='OINK.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='Images\\PORK_Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='OINK')
