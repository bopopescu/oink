# -*- mode: python -*-

block_cipher = None


a = Analysis(['OINK.pyw'],
             pathex=['C:\\Users\\vinay.keerthi\\Google Drive\\Projects\\WFM\\O.I.N.K Report Management System\\Admin\\OINK'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='OINK.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='Images\\oink.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='OINK')
