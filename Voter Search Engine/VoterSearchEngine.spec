# -*- mode: python -*-

block_cipher = None

missing_files = []

for tl in ["GdkPixbuf-2.0.typelib", "GModule-2.0.typelib"] :
    missing_files.append(("C:\Python34\Lib\site-packages\gnome\lib\girepository-1.0", "./gi_typelibs"))

a = Analysis(['obfuscated.py'],
             pathex=['C:\\Users\\BRAHMDEV\\Desktop\\Voter Search Engine'],
             binaries=missing_files,
             datas=[('FileStyle.css','.'), ('AgeSearch.png','.'), ('android.png','.'), ('config.cfg','.'), ('candidate.jpg','.'), ('CasteSearch.png','.'), ('contact_us.png','.'), ('duplicate.png','.'), ('evm-bg.png','.'), ('GenSearch.png','.'), ('Header2.png','.'), ('Hof.png','.'), ('voter slip.png','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='obfuscated',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='obfuscated')


