"""
Groundwater flow model

2D steady-state groundwater flow in a soil region with a notch in the top
surface. Refactored from the CALFEM example gwflow.py into a reusable class
without any plotting or user interface code.
"""

import math

import numpy as np

import calfem.core as cfc
import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.utils as cfu


class GroundwaterModel:
    """Groundwater flow in a rectangular soil region with a notch"""

    # Boundary markers used in the geometry

    RIGHT_MARKER = 80
    LEFT_MARKER = 90

    def __init__(self):
        """Create a model with the default parameters from gwflow.py"""

        # Geometry (m)

        self.w = 100.0           # Width of the region
        self.h = 10.0            # Height of the region
        self.t = 5.0             # Width of the notch
        self.d = 5.0             # Depth of the notch

        # Material

        self.kx = 1.0            # Permeability in x (m/s)
        self.ky = 1.0            # Permeability in y (m/s)

        # Boundary conditions (m)

        self.head_left = 10.0
        self.head_right = 0.0

        # Mesh

        self.el_size_factor = 1.0

        # Results, set by solve()

        self.geometry = None
        self.coords = None
        self.edof = None
        self.dofs = None
        self.bdofs = None
        self.a = None
        self.r = None
        self.flow = None

    def create_geometry(self):
        """Create the geometry of the region"""

        w, h, t, d = self.w, self.h, self.t, self.d

        g = cfg.Geometry()

        g.point([0.0, 0.0])                     # 0
        g.point([w, 0.0])                       # 1
        g.point([w, h])                         # 2
        g.point([w / 2 + t / 2, h])             # 3
        g.point([w / 2 + t / 2, h - d])         # 4
        g.point([w / 2 - t / 2, h - d])         # 5
        g.point([w / 2 - t / 2, h])             # 6
        g.point([0.0, h])                       # 7

        g.spline([0, 1])                                # 0
        g.spline([1, 2])                                # 1
        g.spline([2, 3], marker=self.RIGHT_MARKER)      # 2
        g.spline([3, 4])                                # 3
        g.spline([4, 5])                                # 4
        g.spline([5, 6])                                # 5
        g.spline([6, 7], marker=self.LEFT_MARKER)       # 6
        g.spline([7, 0])                                # 7

        g.surface([0, 1, 2, 3, 4, 5, 6, 7])

        return g

    def create_mesh(self, geometry):
        """Mesh the geometry with 4-node quadrilateral elements"""

        mesh = cfm.GmshMeshGenerator(geometry)
        mesh.el_size_factor = self.el_size_factor
        mesh.el_type = 3
        mesh.dofs_per_node = 1

        return mesh.create()

    def solve(self):
        """Create geometry and mesh, assemble and solve the flow problem"""

        self.geometry = self.create_geometry()

        coords, edof, dofs, bdofs, element_markers = self.create_mesh(self.geometry)

        # Element properties: thickness and integration rule

        ep = [1.0, 1]
        D = np.array([[self.kx, 0.0], [0.0, self.ky]])

        # Assemble the global system

        n_dofs = np.size(dofs)
        ex, ey = cfc.coordxtr(edof, coords, dofs)

        K = np.zeros([n_dofs, n_dofs])

        for el_topo, el_x, el_y in zip(edof, ex, ey):
            Ke = cfc.flw2i4e(el_x, el_y, ep, D)
            cfc.assem(el_topo, K, Ke)

        # Boundary conditions

        f = np.zeros([n_dofs, 1])
        bc = np.array([], int)
        bc_val = np.array([], float)

        bc, bc_val = cfu.applybc(bdofs, bc, bc_val, self.RIGHT_MARKER, self.head_right)
        bc, bc_val = cfu.applybc(bdofs, bc, bc_val, self.LEFT_MARKER, self.head_left)

        # Solve

        a, r = cfc.solveq(K, f, bc, bc_val)

        # Element flows

        ed = cfc.extract_eldisp(edof, a)

        flow = []

        for i in range(edof.shape[0]):
            es, et, eci = cfc.flw2i4s(ex[i, :], ey[i, :], ep, D, ed[i, :])
            flow.append(math.sqrt(es[0, 0] ** 2 + es[0, 1] ** 2))

        # Store results

        self.coords = coords
        self.edof = edof
        self.dofs = dofs
        self.bdofs = bdofs
        self.a = a
        self.r = r
        self.flow = np.array(flow)


if __name__ == "__main__":

    model = GroundwaterModel()
    model.solve()

    print(f"Nodes:         {model.coords.shape[0]}")
    print(f"Elements:      {model.edof.shape[0]}")
    print(f"Head range:    {model.a.min():.3f} - {model.a.max():.3f} m")
    print(f"Max flow:      {model.flow.max():.4f}")
