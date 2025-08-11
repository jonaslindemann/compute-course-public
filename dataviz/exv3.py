from vedo import load, show, Volume

# Load your volume (assuming it's already resampled as per previous example)
volume = load("resampled_volume.vti")

print("Volume type:", type(volume))
print("Volume dimensions:", volume.dimensions())

# List available point data arrays
print("\nAvailable point data arrays:")
for name in volume.pointdata.keys():
    array = volume.pointdata[name]
    print(f"  {name}: shape={array.shape}, dtype={array.dtype}")

# List available cell data arrays (if any)
print("\nAvailable cell data arrays:")
for name in volume.celldata.keys():
    array = volume.celldata[name]
    print(f"  {name}: shape={array.shape}, dtype={array.dtype}")

# Select a specific dataset (replace 'dataset_name' with the actual name)
dataset_name = 'Resistivity(log10)'  # Replace this with an actual dataset name from your volume

if dataset_name in volume.pointdata.keys():
    selected_data = volume.pointdata[dataset_name]
    print(f"\nSelected dataset '{dataset_name}' from point data")
elif dataset_name in volume.celldata.keys():
    selected_data = volume.celldata[dataset_name]
    print(f"\nSelected dataset '{dataset_name}' from cell data")
else:
    print(f"\nDataset '{dataset_name}' not found in volume data")
    exit()

print("Selected data shape:", selected_data.shape)
print("Selected data type:", selected_data.dtype)
print("Data range:", selected_data.min(), "to", selected_data.max())

# Visualize the selected dataset
volume.cmap(dataset_name, 'jet')  # Set colormap for the selected dataset

# Option 1: Show volume rendering
show(volume.volume(), axes=1, bg='white', title=f"Volume Rendering of {dataset_name}")

# Option 2: Show orthogonal slices
slices = volume.slice_orthogonal()
show(slices, axes=1, bg='white', title=f"Orthogonal Slices of {dataset_name}")

# Option 3: Show isosurface
# Choose an appropriate isovalue between min and max of your data
isovalue = (selected_data.min() + selected_data.max()) / 2
isosurface = volume.isosurface(value=isovalue)
show(isosurface, axes=1, bg='white', title=f"Isosurface of {dataset_name}")

# Option 4: Interactive slice browser
from vedo import SliceXYZ
slice_browser = SliceXYZ(volume, cmap='jet')
slice_browser.show(axes=1, bg='white', title=f"Interactive Slice Browser for {dataset_name}")