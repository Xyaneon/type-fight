from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ['fonts/', 'graphics/', 'sounds/', 'music/'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

shortcut_table = [
    ("DesktopShortcut",         # Shortcut
     "DesktopFolder",           # Directory_
     "TypeFight!",              # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]typefight.exe",# Target
     None,                      # Arguments
     None,                      # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

executables = [
    Executable('typefight.py')
]

setup(name='TypeFight',
      version = '0.1',
      description = 'A typing game with fighting robots',
      options = dict(build_exe = buildOptions, bdist_msi = bdist_msi_options),
      executables = executables)
