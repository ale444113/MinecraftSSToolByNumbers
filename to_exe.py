from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('main.py', base=base, target_name = 'numbersstool.exe')
]

setup(name='SSToolByNumbers',
      version = '1.0',
      description = 'Esta es un scanner usado como ss tool creado por ale444113',
      options = {'build_exe': build_options},
      executables = executables)
