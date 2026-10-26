project('fstats', 'c', 'fortran',
  version : '0.1.0',
  meson_version : '>= 1.1.0',
  default_options : ['warning_level=1', 'buildtype=release'])

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

# --- Include directories for NumPy and f2py

incdir_numpy = run_command(py,
  ['-c', 'import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
  ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'],
  check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy, incdir_f2py)

# --- Let f2py generate the C wrapper for the Fortran module

fstats_source = custom_target('fstatsmodule.c',
  input : ['src/fstats.f90'],
  output : ['fstatsmodule.c', 'fstats-f2pywrappers2.f90'],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', '-m', 'fstats', '--lower', '--build-dir', '@OUTDIR@']
)

# --- Compile the Fortran code and the wrapper into an extension module

py.extension_module('fstats',
  ['src/fstats.f90', fstats_source, incdir_f2py / 'fortranobject.c'],
  include_directories : inc_np,
  dependencies : py_dep,
  install : true
)
