from vedo import Volume, show, dataurl

# Load a sample volume data
vol = Volume(dataurl + "embryo.tif")

# Display the volume
show(vol, "Volume Rendering", axes=1)