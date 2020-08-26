# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:03:31 2017

@author: Jonas Lindemann
"""

import numpy as np
import matplotlib.pyplot as plt
import perlin2d as pn
import pyvtk as vtk
    
if __name__ == "__main__":

    noise = pn.generate_perlin_noise_2d((256, 256), (8, 8))

    pointdata = vtk.PointData(vtk.Scalars(noise.reshape((256*256,))))
    data = vtk.VtkData(vtk.StructuredPoints([256,256]), pointdata)
    data.tofile('perlin', 'ascii')




