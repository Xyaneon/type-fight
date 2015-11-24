from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ['fonts/', 'graphics/', 'sounds/', 'music/', 'help/'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

shortcut_table = [
    ("DesktopShortcut",         # Shortcut
     "DesktopFolder",           # Directory_
     "TypeFight!",              # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]typefight.exe",# Target
     None,                      # Arguments
     "A typing game with fighting robots.",  # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     ),
    ("ProgramMenuShortcut",         # Shortcut
     "ProgramMenuFolder",           # Directory_
     "TypeFight!",              # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]typefight.exe",# Target
     None,                      # Arguments
     "A typing game with fighting robots.",  # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     ),
    ("ProgramMenuHelpShortcut",         # Shortcut
     "ProgramMenuFolder",           # Directory_
     "TypeFight! Help",              # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]help/typefight.html",# Target
     None,                      # Arguments
     "TypeFight! electronic instruction manual.",  # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data, 'upgrade_code': '{bd944f23-280b-49c4-8c25-ebc5823f18e0}'}

executables = [
    Executable('typefight.py', base=base)
]

setup(name='TypeFight',
      version = '0.2',
      description = 'A typing game with fighting robots',
      options = dict(build_exe = buildOptions, bdist_msi = bdist_msi_options),
      executables = executables)
