# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:03:31 2017

@author: Jonas Lindemann
"""

import numpy as np
import matplotlib.pyplot as plt
import perlin3d as pn
import pyvtk as vtk
    
if __name__ == "__main__":

    noise = pn.generate_perlin_noise_3d((128, 128, 128), (8, 8, 8))

    pointdata = vtk.PointData(vtk.Scalars(noise.reshape((128*128*128,))))
    data = vtk.VtkData(vtk.StructuredPoints([128,128,128]), pointdata)
    data.tofile('perlin3d', 'ascii')




