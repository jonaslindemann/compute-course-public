
import mf_mixed

mf_mixed.f2py_setup()
mf_mixed.f2py_compile('fortmod', ['simple.f90'])

from numpy import *
from fortmod import *

print("-------------------------------------")
print(simple.__doc__)
print("-------------------------------------")
print()

a = 2
b = 3
c = simple(a, b)

print("c =", c)