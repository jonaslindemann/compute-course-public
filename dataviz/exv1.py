from vedo import dataurl, Volume, load
from vedo.applications import IsosurfaceBrowser

print(dataurl+'head.vti')
vol = Volume('perlin3d.vti')
#vol = Volume(load("perlin3d.vtk"))

# IsosurfaceBrowser(Plotter) instance:
plt = IsosurfaceBrowser(vol, use_gpu=True, c='gold')
plt
plt.show(axes=7, bg2='lb').close()