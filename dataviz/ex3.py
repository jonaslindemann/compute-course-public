# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:03:31 2017

@author: Jonas Lindemann
"""
import numpy as np
import matplotlib.pyplot as plt
import pyvtk as vtk
import os

image_dir = "./CTHead"
file_templ = "CThead.{}"

image_data = np.zeros((256,256,113), np.uint16, order="F")

print(image_data.size)

for i in range(1,114):
    image_filename = os.path.join(image_dir, file_templ.format(i))
    f = open(image_filename, "rb")
    raw_data = np.fromfile(f, dtype=np.uint16)
    f.close()
    
    image_data[:,:,i-1] = raw_data.reshape(256,256)
    

plt.imshow(image_data[:,:,50])
    
print("Saving to VTK")
pointdata = vtk.PointData(vtk.Scalars(image_data.reshape(256*256*113)))
data = vtk.VtkData(vtk.StructuredPoints([113,256,256]), pointdata)
data.tofile('cthead','ascii')

