# Exercise 7 - Reading uvw data from a text file

In this exercise you need to read the structure and flowfield from the uvw.dat file. This file contains 6 columns of data. The first columns x y z positions and last columns are vector data. For more information see:

http://www.idvbook.com/teaching-aid/data-sets/the-uvw-data-set/

The first rows of the file is shown below:

    variables="x","y","z","u","v","w"
    zone i=96,j=65,k=48,f=point
    0 -1 0 -7.00895e-05 2.28715e-05 7.11905e-05
    0.0327249 -1 0 -8.01278e-05 1.89072e-05 4.83821e-05
    0.0654498 -1 0 -6.8715e-05 8.60358e-06 -1.31806e-06
    0.0981748 -1 0 -3.79768e-05 -4.03025e-06 -5.09628e-05
    0.1309 -1 0 -8.62436e-06 -1.93002e-05 -9.18307e-05
    ...

To read the dataset use the loadtxt(...) function in NumPy to read the data from the file. Use the skiprows argument to let loadtxt() skip the header information.

From the loaded array extract two arrays, points and vectors. Use indexing/slicing to accomplish this.

PyVTK can only handle lists as input, so the arrays must be converted to lists before being passed to PyVTK. This can be done using the .tolist()-method in the array class.

Writing data to PyVTK is then done using the following code:

    pointdata = vtk.PointData(vtk.Vectors(vectors.tolist()))
    data = vtk.VtkData(vtk.StructuredPoints([96, 65, 48]), pointdata)
    data.tofile('uvw','ascii')

In this example the coordinates is ignored and vectors are visualised on a structured grid.

# Exercise 8 - Colorado elevation grid

Add the following code to your elevation exercise to write a file suitable for visualisation in VTK:

    pointdata = vtk.PointData(vtk.Scalars(x))
    data = vtk.VtkData(vtk.StructuredPoints([400,400]), pointdata)
    data.tofile('elevation','ascii')

x is the points read from the elevation file, not reshaped.
