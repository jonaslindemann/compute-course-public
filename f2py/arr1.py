# -*- coding: utf-8 -*-

import os
import numpy as np
import fortran_utils as utils

# Add the path to the directory containing the Fortran runtime DLL to the system path

utils.f2py_setup()

if utils.f2py_compile("fortmod", ["arr1.f90"])!=0:
    print("Compilation failed")
    exit()

from fortmod import *

print("-------------------------------------")
print(matrix_multiply.__doc__)
print("-------------------------------------")
print()

A = np.ones((6,6), 'f', order='F') * 10.0
B = np.ones((6,6), 'f', order='F') * 20.0
C = np.zeros((6,6), 'f', order='F')

print("id of C before multiply =",id(C))

C = matrix_multiply(A, B)

print("id of C after multiply =",id(C))

print(C)