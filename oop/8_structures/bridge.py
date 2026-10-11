# -*- coding: utf-8 -*-

from structure import Structure, Spring, PinSupport, RollerSupport

def create_bridge(n_panels=6, panel_width=2.0, height=2.0, bearing_stiffness=5e7):
    """
    A Pratt truss bridge resting on two rubber bearings (springs).

    Returns the structure and the list of deck nodes (the bottom chord), where
    traffic loads are applied.
    """
    s = Structure()

    deck = [s.add_node(i * panel_width, 0.0) for i in range(n_panels + 1)]
    top = [None] + [s.add_node(i * panel_width, height) for i in range(1, n_panels)] + [None]

    for i in range(n_panels):
        s.add_bar(deck[i], deck[i + 1])                      # bottom chord

    for i in range(1, n_panels - 1):
        s.add_bar(top[i], top[i + 1])                        # top chord

    for i in range(1, n_panels):
        s.add_bar(deck[i], top[i])                           # verticals

    s.add_bar(deck[0], top[1])                               # end diagonals
    s.add_bar(top[n_panels - 1], deck[n_panels])

    for i in range(1, n_panels):                             # diagonals, sloping down towards the middle
        if i < n_panels / 2:
            s.add_bar(top[i], deck[i + 1])
        elif i > n_panels / 2:
            s.add_bar(top[i], deck[i - 1])

    # Bearings: a spring from each end of the bridge down to a fixed ground node.

    for node in [deck[0], deck[-1]]:
        ground = s.add_node(node.x, -1.0)
        s.add_support(PinSupport(ground))
        s.add_spring(node, ground, bearing_stiffness)

    # Something has to stop the bridge from sliding sideways.

    s.add_support(RollerSupport(deck[0], free="y"))

    return s, deck

def set_bearing_stiffness(structure, k):
    for element in structure.elements:
        if isinstance(element, Spring):
            element.k = k
