# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:19:00 2017

@author: Jonas Lindemann
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50

plt.hist(x, num_bins, normed=1)

plt.xlabel('Smarts')
plt.ylabel('Probability density')

plt.show()