# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:03:31 2017

@author: Jonas Lindemann
"""
import numpy as np
import matplotlib.pyplot as plt
import pyvtk as vtk
import os

f = open("colorado_elev.vit", "rb")  # reopen the file
f.seek(268, os.SEEK_SET)  # seek

x = np.fromfile(f, dtype=np.ubyte)  # read the data into numpy

elevation = np.reshape(x, (400,400))
plt.imshow(elevation)

plt.show()

pointdata = vtk.PointData(vtk.Scalars(x))
data = vtk.VtkData(vtk.StructuredPoints([400,400]), pointdata)
data.tofile('elevation','ascii')

