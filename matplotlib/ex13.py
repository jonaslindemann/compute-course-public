# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:19:00 2017

@author: Jonas Lindemann
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,2.0, 0.01)
y = np.exp(x)

plt.figure(1)
plt.yscale('log')
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x, y, 'r-')

plt.show()