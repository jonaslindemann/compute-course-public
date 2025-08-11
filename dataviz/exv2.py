from vedo import load, Volume, Plotter, Text2D
import numpy as np

# Load the VTK file and convert to Volume if necessary
vol = load("perlin3d.vtk")
if not isinstance(vol, Volume):
    vol = Volume(vol)

# Function to update the isosurface
def update_isosurface(widget, event):
    value = widget.GetRepresentation().GetValue()
    iso.threshold(value)
    txt.text(f"Isovalue: {value:.1f}")
    plt.render()

# Get the scalar range
scalar_range = vol.scalar_range()

if scalar_range is None:
    print("Unable to determine scalar range. Please check your data.")
    exit()

# Create a plotter
plt = Plotter(bg='black', bg2='lb', axes=7)

# Create initial isosurface
initial_value = (scalar_range[0] + scalar_range[1]) / 2
iso = vol.isosurface(initial_value).color('gold')

# Add the isosurface to the plotter
plt.add(iso)

# Create a slider widget
plt.add_slider(
    update_isosurface,
    scalar_range[0],
    scalar_range[1],
    value=initial_value,
    pos="bottom-right",
    title="Isovalue",
    show_value=True
)

# Add text to display current isovalue
txt = Text2D(f"Isovalue: {initial_value:.1f}", pos="top-left")
plt.add(txt)

# Show the plot
plt.show().close()