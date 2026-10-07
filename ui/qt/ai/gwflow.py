# -*- coding: utf-8 -*-

import math

import calfem.core as cfc
import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis as cfv
import calfem.utils as cfu

import numpy as np

# ------ Problem parameters ------

w = 100.0
h = 10.0
t = 5.0
d = h/2.0

D = np.identity(2, 'float') * 1.0
ep = [1.0, 1]

# ------ Create geometry instance ------------

g = cfg.Geometry()

g.point([0, 0])           # 0
g.point([w, 0])           # 1
g.point([w, h])           # 2
g.point([w-w/2.+t/2., h]) # 3
g.point([w-w/2+t/2, h-d]) # 4
g.point([w-w/2-t/2, h-d]) # 5
g.point([w-w/2-t/2, h])   # 6
g.point([0.,h])           # 7

g.spline([0, 1])            #0
g.spline([1, 2])            #1
g.spline([2, 3], marker=80) #2
g.spline([3, 4])            #3
g.spline([4, 5])            #4
g.spline([5, 6])            #5
g.spline([6, 7], marker=90) #6
g.spline([7, 0])            #7

g.surface([0,1,2,3,4,5,6,7])

# ------ Mesh generation ------------

elType = 3
dofsPerNode= 1 

meshGen = cfm.GmshMeshGenerator(g)
meshGen.elSizeFactor = 1.0     # Factor that changes element sizes.
meshGen.elType = elType
meshGen.dofsPerNode = dofsPerNode

coords, edof, dofs, bdofs, elementmarkers = meshGen.create()

# ------ Assemble system ------------

nDofs = nDofs = np.size(dofs)
ex, ey = cfc.coordxtr(edof, coords, dofs)
K = np.zeros([nDofs,nDofs])

for eltopo, elx, ely in zip(edof, ex, ey):
	Ke = cfc.flw2i4e(elx, ely, ep, D)
	cfc.assem(eltopo, K, Ke)
 
# ------ Forces and boundary conditions ------------

f = np.zeros([nDofs,1])
bc = np.array([], int)
bcVal = np.array([], int)

bc, bcVal = cfu.applybc(bdofs, bc, bcVal, 80, 0.0)
bc, bcVal = cfu.applybc(bdofs, bc, bcVal, 90, 10.0)

# ------ Solve equation system ------------

a,r = cfc.solveq(K,f,bc,bcVal)

# ------ Calculate element forces ------------

ed = cfc.extractEldisp(edof,a)

maxFlow = []
for i in range(edof.shape[0]): 
	es, et, eci = cfc.flw2i4s(ex[i,:], ey[i,:], ep, D, ed[i,:]) 
	maxFlow.append( 
		math.sqrt( math.pow(es[0,0],2) + math.pow(es[0,1],2)) 
	) 
 
# ------ Draw results ------------

cfv.figure() 
cfv.drawGeometry(g, title="Geometry")

cfv.figure()
cfv.drawElementValues(maxFlow, coords, edof, dofsPerNode, elType, None, 
                      doDrawMesh=False, title="Max flows")

cfv.figure() 
cfv.drawMesh(coords, edof, dofsPerNode, elType, filled=True, title="Mesh") 

cfv.figure() 
cfv.drawNodalValues(a, coords, edof, dofsPerNode, 
	elType, doDrawMesh=False, title="Nodal values")

cfv.colorBar().SetLabel("Flow")

print("Done drawing...")

cfv.showAndWait()