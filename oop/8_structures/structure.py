# -*- coding: utf-8 -*-
"""
Linear static analysis of 2D structures built from bars and springs.

This module contains only the model and the solver. It doesn't import any
graphics library, so the same classes are used by 01_bridge_plot.py
(matplotlib) and 02_bridge_py5.py (interactive py5).
"""

import numpy as np

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = None    # set by Structure.add_node()
        self.ux = 0.0        # displacements, set by Structure.solve()
        self.uy = 0.0

    @property
    def dofs(self):
        """The global degrees of freedom of this node: [x, y]."""
        return [2*self.index, 2*self.index + 1]

    def __repr__(self):
        return "Node(" + str(self.x) + ", " + str(self.y) + ")"


class AxialElement:
    """
    Base class for elements that only carry force along the line between their
    two nodes. Subclasses only have to say how stiff they are.
    """

    def __init__(self, node0, node1):
        self.node0 = node0
        self.node1 = node1
        self.force = 0.0     # axial force after solve(), positive = tension

    @property
    def length(self):
        return np.hypot(self.node1.x - self.node0.x, self.node1.y - self.node0.y)

    @property
    def dofs(self):
        return self.node0.dofs + self.node1.dofs

    def axial_stiffness(self):
        raise NotImplementedError("Subclasses of AxialElement must implement axial_stiffness()")

    def elongation_vector(self):
        """Elongation of the element = elongation_vector() @ [ux0, uy0, ux1, uy1]."""
        c = (self.node1.x - self.node0.x) / self.length
        s = (self.node1.y - self.node0.y) / self.length
        return np.array([-c, -s, c, s])

    def stiffness_matrix(self):
        b = self.elongation_vector()
        return self.axial_stiffness() * np.outer(b, b)

    def compute_force(self, u):
        self.force = self.axial_stiffness() * (self.elongation_vector() @ u[self.dofs])


class Bar(AxialElement):
    """A bar with Young's modulus E [Pa] and cross-section area A [m2]."""

    def __init__(self, node0, node1, E=210e9, A=2e-3):
        super().__init__(node0, node1)
        self.E = E
        self.A = A

    def axial_stiffness(self):
        return self.E * self.A / self.length

    @property
    def stress(self):
        return self.force / self.A

    def __repr__(self):
        return "Bar(" + str(self.node0.index) + " -> " + str(self.node1.index) + ")"


class Spring(AxialElement):
    """A spring with stiffness k [N/m], independent of its length."""

    def __init__(self, node0, node1, k):
        super().__init__(node0, node1)
        self.k = k

    def axial_stiffness(self):
        return self.k

    def __repr__(self):
        return "Spring(" + str(self.node0.index) + " -> " + str(self.node1.index) + ")"


class Support:
    """Base class for supports. Subclasses decide which directions are fixed."""

    def __init__(self, node):
        self.node = node

    def fixed_dofs(self):
        raise NotImplementedError("Subclasses of Support must implement fixed_dofs()")


class PinSupport(Support):
    """Fixed in both x and y."""

    def fixed_dofs(self):
        return self.node.dofs


class RollerSupport(Support):
    """Fixed in one direction, free to roll in the other ("x" or "y")."""

    def __init__(self, node, free="x"):
        super().__init__(node)
        self.free = free

    def fixed_dofs(self):
        if self.free == "x":
            return [self.node.dofs[1]]
        else:
            return [self.node.dofs[0]]


class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.supports = []
        self.loads = {}         # node -> [fx, fy]
        self.reactions = None   # support forces, set by solve()

    def add_node(self, x, y):
        node = Node(x, y)
        node.index = len(self.nodes)
        self.nodes.append(node)
        return node

    def add_element(self, element):
        self.elements.append(element)
        return element

    def add_bar(self, node0, node1, E=210e9, A=2e-3):
        return self.add_element(Bar(node0, node1, E, A))

    def add_spring(self, node0, node1, k):
        return self.add_element(Spring(node0, node1, k))

    def add_support(self, support):
        self.supports.append(support)
        return support

    def add_load(self, node, fx, fy):
        self.loads[node] = [fx, fy]

    def clear_loads(self):
        self.loads = {}

    def solve(self):
        n_dofs = 2 * len(self.nodes)

        K = np.zeros((n_dofs, n_dofs))
        f = np.zeros(n_dofs)

        # Every element adds its own stiffness matrix. The loop doesn't know
        # or care whether an element is a Bar, a Spring or something else.

        for element in self.elements:
            K[np.ix_(element.dofs, element.dofs)] += element.stiffness_matrix()

        for node, (fx, fy) in self.loads.items():
            f[node.dofs] += [fx, fy]

        fixed = sorted({dof for support in self.supports for dof in support.fixed_dofs()})
        free = [dof for dof in range(n_dofs) if dof not in fixed]

        K_free = K[np.ix_(free, free)]

        if np.linalg.cond(K_free) > 1e12:
            raise ValueError("The structure is a mechanism, it can move without deforming. Add bars or supports.")

        u = np.zeros(n_dofs)
        u[free] = np.linalg.solve(K_free, f[free])

        for node in self.nodes:
            node.ux, node.uy = u[node.dofs]

        for element in self.elements:
            element.compute_force(u)

        self.reactions = K @ u - f

        return u

    def max_displacement(self):
        return max(np.hypot(node.ux, node.uy) for node in self.nodes)
