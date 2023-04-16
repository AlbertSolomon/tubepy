from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('tubepy/setup.py', base=base, target_name = 'tubepy.msi')
]

setup(name='tubepy',
      version = '1.0.0-beta',
      description = 'YouTube video downloader in python 😎',
      options = {'build_exe': build_options},
      executables = executables)
