# -*- coding: utf-8 -*-

import os

f2py_mingw_path = "E:\\Qt\\Tools\\mingw1120_64\\bin"

def f2py_setup():
    if os.name == 'nt':
        os.add_dll_directory(f2py_mingw_path)

def f2py_compile(f2py_module_name, f2py_source_files, compiler_flags="-Wtabs"):
    print(f"Running: f2py -m {f2py_module_name} -c {' '.join(f2py_source_files)} --f90flags={compiler_flags}")
    return os.system(f"f2py -m {f2py_module_name} -c {' '.join(f2py_source_files)} --f90flags={compiler_flags}")