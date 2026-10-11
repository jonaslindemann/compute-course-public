"""Read structured grid data and show
the associated vector and scalar fields"""
from vedo import *

import numpy as np
import pandas as pd

# Read cvs data
df = pd.read_csv("scalar.csv")
pts = np.c_[df['X32'], df['Y32'], df['Z32']]
s = np.c_[df['S']]
#vecs= np.c_[df['u'], df['v'], df['w']]

print(pts.shape)

points = Points(pts)
points.pointdata["S"] = s
points.cmap('jet', input_array='S').addScalarBar(title='S')

spheres = Spheres(points, r=0.001*s)

show([spheres]).close()
