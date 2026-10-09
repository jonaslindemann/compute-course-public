# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from structure import Spring
from bridge import create_bridge

LOAD = 100e3        # N, downwards
LOAD_NODE = 3       # index in the deck list, 3 = middle of the bridge

bridge, deck = create_bridge()
bridge.add_load(deck[LOAD_NODE], 0.0, -LOAD)
bridge.solve()

print("Element               Force [kN]")
for element in bridge.elements:
    print(f"{repr(element):20s} {round(element.force / 1e3, 1) + 0.0:10.1f}")  # + 0.0 turns -0.0 into 0.0

print()
print(f"Sum of vertical reactions: {bridge.reactions[1::2].sum() / 1e3:.1f} kN")
print(f"Max displacement:          {bridge.max_displacement() * 1e3:.2f} mm")

# Displacements are a few mm, so scale them up to make them visible.

scale = 0.4 / bridge.max_displacement()

undeformed = []
deformed = []
forces = []
springs = []

for element in bridge.elements:
    n0, n1 = element.node0, element.node1

    undeformed.append([(n0.x, n0.y), (n1.x, n1.y)])
    line = [(n0.x + scale * n0.ux, n0.y + scale * n0.uy), (n1.x + scale * n1.ux, n1.y + scale * n1.uy)]

    if isinstance(element, Spring):
        springs.append(line)
    else:
        deformed.append(line)
        forces.append(element.force / 1e3)

fig, ax = plt.subplots(figsize=(11, 5))

ax.add_collection(LineCollection(undeformed, colors="lightgray", linewidths=1, linestyles="dashed"))
ax.add_collection(LineCollection(springs, colors="tab:green", linewidths=3))

limit = max(abs(force) for force in forces)
bars = LineCollection(deformed, cmap="coolwarm", linewidths=3)
bars.set_array(forces)
bars.set_clim(-limit, limit)
ax.add_collection(bars)
fig.colorbar(bars, ax=ax, orientation="horizontal", shrink=0.6, pad=0.15,
             label="Axial force [kN]  (blue = compression, red = tension)")

load_node = deck[LOAD_NODE]
x = load_node.x + scale * load_node.ux
y = load_node.y + scale * load_node.uy
ax.annotate(f"{LOAD / 1e3:.0f} kN", xy=(x, y), xytext=(x, 3.0), ha="center",
            arrowprops=dict(arrowstyle="->", linewidth=2))

ax.set_title(f"Pratt truss bridge, displacements scaled {scale:.0f}x")
ax.set_aspect("equal")
ax.autoscale()
ax.margins(0.08)
ax.set_ylim(-1.5, 3.5)      # room for the load arrow
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")

fig.tight_layout()
plt.show()
