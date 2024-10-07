# -*- coding: utf-8 -*-

import os
import numpy as np
import mf_mixed

mf_mixed.f2py_setup()
mf_mixed.f2py_compile('fortmod', ['arr1.f90'])

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