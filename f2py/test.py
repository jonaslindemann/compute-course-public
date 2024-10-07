import mf_mixed

mf_mixed.f2py_setup()
mf_mixed.f2py_compile('fortmod', ['matrix.f90'])

from numpy import *
from fortmod import *

print(matrix.matrix_multiply2.__doc__)

A = ones((10,10), 'float32', order='F') * 10.0
B = ones((10,10), 'float32', order='F') * 20.0
C = zeros((10,10), 'float32', order='F')

print("id of C before multiply =",id(C))

matrix.matrix_multiply2(A, B, C)

print("id of C after multiply =",id(C))

print(C)