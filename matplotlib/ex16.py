# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:47:33 2017

@author: Jonas Lindemann
"""

import matplotlib.pyplot as plt
import numpy as np

for color in ['red', 'green', 'blue']:
    n = 750
    x, y = np.random.rand(2, n)
    scale = 200.0 * np.random.rand(n)
    plt.scatter(x, y, c=color, s=scale, label=color,
                alpha=0.3, edgecolors='none')

plt.legend()
plt.grid(True)

plt.show()