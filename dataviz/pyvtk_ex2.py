#!/usr/bin/env python

from pyvtk import *

vtk = VtkData(StructuredPoints([3,4,6]),
              PointData(Scalars([0,0,0,0,0,0,0,0,0,0,0,0,
                                 0,5,10,15,20,25,25,20,15,10,5,0,
                                 0,10,20,30,40,50,50,40,30,20,10,0,
                                 0,10,20,30,40,50,50,40,30,20,10,0,
                                 0,5,10,15,20,25,25,20,15,10,5,0,
                                 0,0,0,0,0,0,0,0,0,0,0,0
                                 ])))

vtk.tofile('example2')
vtk.tofile('example2b','binary')

vtk = VtkData('example2',only_structure = 1)
def f(x,y,z):
    return x*y*z
vtk.point_data.append(vtk.structure.Scalars(f,'x*y*z'))
vtk.tofile('example2f_sp')

pp = [(i,j,k) for k in range(6) for j in range(4) for i in range(3)]
vtk = VtkData(StructuredGrid([3,4,6],pp))
vtk.point_data.append(vtk.structure.Scalars(f,'x*y*z'))
vtk.tofile('example2f_sg')

vtk = VtkData(RectilinearGrid(range(3),range(4),range(6)))
vtk.point_data.append(vtk.structure.Scalars(f,'x*y*z'))
vtk.tofile('example2f_rg')

