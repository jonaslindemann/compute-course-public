# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:03:31 2017

@author: Jonas Lindemann
"""

import numpy as np

import matplotlib.pyplot as plt
import perlin3d as pn

from pyevtk.hl import gridToVTK, imageToVTK

    
from vedo import Volume, show, load, Plotter
from vedo.applications import IsosurfaceBrowser, Slicer3DPlotter, Slicer3DTwinPlotter, Slicer2DPlotter, RayCastPlotter, Browser, FreeHandCutPlotter, MorphPlotter, SplinePlotter, AnimationPlayer

if __name__ == "__main__":

    #noise = pn.generate_perlin_noise_3d((128, 128, 128), (8, 8, 8))

    #imageToVTK("perlin3d", origin = (0,0,0), spacing = (1,1,1), pointData = {"noise" : noise})

    vol = Volume("resampled_volume.vti")

    # Select a specific data field in the volume to visualize
    data_field = vol.pointdata["Resistivity(log10)"]
    vol.pointdata.select("Resistivity(log10)")
    vol.shade(True)
    
    #mesh = load("perlin3d.vtk")
    dam = load("dam.vtk")
    dam.pointdata.select("Resistivity(log10)")
    #dam_mesh = dam.tomesh()
    #dam_volume = Volume(dam.tomesh())

    #print("Loaded object type:", type(dam_mesh))
    #print("Number of points:", dam_mesh.npoints)
    #print("Number of cells:", dam_mesh.ncells)

    #plt = IsosurfaceBrowser(vol, use_gpu=True, c='gold')
    #plt = Slicer3DPlotter(vol, cmaps=("gist_ncar_r", "hot_r", "bone"))
    #plt = RayCastPlotter(vol)
    #plt  = FreeHandCutPlotter(dam.tomesh())
    
    #plt = Plotter(bg='black', bg2='lb', axes=7)
    #plt.add(dam_volume)

    plt.show(axes=7, bg2='lb').close()


