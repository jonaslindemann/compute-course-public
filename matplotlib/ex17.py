# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:52:04 2017

@author: Jonas Lindemann
"""

import matplotlib.pyplot as plt
import numpy as np

N = 100

x = np.linspace(-6.0, 6.0, N)
y = np.linspace(-6.0, 6.0, N)

X, Y = np.meshgrid(x, y)

z = np.sin(0.5*X*Y)

plt.contourf(X, Y, z, cmap=plt.cm.RdBu)
plt.colorbar()

plt.show()