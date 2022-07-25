import PyInstaller.__main__

PyInstaller.__main__.run([
    'launch.py',
    '--onefile',
    '--windowed',
    '--collect-data=biostats',
    '--collect-binaries=biostats',
    '--hidden-import=openpyxl',
    '--hidden-import=pyreadstat',
    '--hidden-import=tabulate',
    '--icon=assets\icon.ico'
])