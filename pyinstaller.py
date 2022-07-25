import PyInstaller.__main__

PyInstaller.__main__.run([
    'launch.py',
    '--onefile',
    '--console',
    '--collect-data=biostats',
    '--collect-binaries=biostats',
    '--hidden-import=openpyxl',
    '--hidden-import=pyreadstat',
    '--hidden-import=tabulate',
    '--icon=assets\icon.ico',
    # bug fix
    '--hidden-import=PIL._tkinter_finder', 
    '--hidden-import=pyreadstat._readstat_writer',
    '--hidden-import=pyreadstat.worker',
    '--hidden-import=matplotlib.backends.backend_pdf',
    '--hidden-import=matplotlib.backends.backend_svg',
    '--hidden-import=matplotlib.backends.backend_ps'
])