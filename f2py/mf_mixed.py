# -*- coding: utf-8 -*-

import os

# ---- 1. Replace the following path with corresponding path in your system ----
f2py_mingw_path = "C:\\Qt\\Tools\\mingw1120_64\\bin"

# ---- 2. Replace the following flags with corresponding flags in your system ----
#f2py_opt_flags = '-Wall -Wextra -Wimplicit-interface -fPIC -O3 -march=native -ffast-math -funroll-loops -fopenmp'
f2py_opt_flags = '-Wall -Wextra -Wimplicit-interface -fPIC -O3 -march=native -ffast-math -funroll-loops -fopenmp -ffree-line-length-none'
#f2py_opt_flags = '-Wall -Wextra -Wimplicit-interface -O3 -march=native'
f2py_link_flags = '-lgomp'

def f2py_setup():
    if os.name == 'nt':
        os.add_dll_directory(f2py_mingw_path)

def f2py_compile(f2py_module_name, f2py_source_files):
    source_files_string = ' '.join(f2py_source_files)
    print(f'Running: f2py -m {f2py_module_name} -c {source_files_string} --f90flags="{f2py_opt_flags}" {f2py_link_flags}')
    return os.system(f'f2py -m {f2py_module_name} -c {source_files_string} --f90flags="{f2py_opt_flags}" {f2py_link_flags}')