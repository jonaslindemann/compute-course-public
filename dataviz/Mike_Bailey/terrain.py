# state file generated using paraview version 5.1.2

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1250, 921]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [0.0, 11.96600000000035, 1668.747]
renderView1.StereoType = 0
renderView1.CameraPosition = [-21608.306504673146, -15177.943521069697, 29475.087306440677]
renderView1.CameraFocalPoint = [-1014.5286225469237, -1369.5587211901707, 298.81195558855103]
renderView1.CameraViewUp = [0.608146780288207, 0.45999977029365136, 0.6469603581015418]
renderView1.CameraParallelScale = 9909.863949044608
renderView1.Background = [0.32, 0.34, 0.43]

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
terraincsv = CSVReader(FileName=['Y:\\ParaView\\Data\\terrain.csv'])

# create a new 'Table To Structured Grid'
tableToStructuredGrid1 = TableToStructuredGrid(Input=terraincsv)
tableToStructuredGrid1.WholeExtent = [0, 511, 0, 360, 0, 0]
tableToStructuredGrid1.XColumn = 'UTMx512'
tableToStructuredGrid1.YColumn = 'UTMy361'
tableToStructuredGrid1.ZColumn = 'Z'

# create a new 'Transform'
transform1 = Transform(Input=tableToStructuredGrid1)
transform1.Transform = 'Transform'

# init the 'Transform' selected for 'Transform'
transform1.Transform.Translate = [0.0, 0.0, 1.75220133095286]
transform1.Transform.Scale = [1.0, 1.0, 0.686659275580685]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get color transfer function/color map for 'Elevation'
elevationLUT = GetColorTransferFunction('Elevation')
elevationLUT.RGBPoints = [5.592, 0.231373, 0.298039, 0.752941, 1668.747, 0.865003, 0.865003, 0.865003, 3331.902, 0.705882, 0.0156863, 0.14902]
elevationLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'Elevation'
elevationPWF = GetOpacityTransferFunction('Elevation')
elevationPWF.Points = [5.592, 0.0, 0.5, 0.0, 3331.902, 1.0, 0.5, 0.0]
elevationPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from transform1
transform1Display = Show(transform1, renderView1)
# trace defaults for the display properties.
transform1Display.ColorArrayName = ['POINTS', 'Elevation']
transform1Display.LookupTable = elevationLUT
transform1Display.Specular = 1.0
transform1Display.OSPRayScaleArray = 'Elevation'
transform1Display.OSPRayScaleFunction = 'PiecewiseFunction'
transform1Display.GlyphType = 'Arrow'
transform1Display.ScalarOpacityUnitDistance = 345.9646504027096

# show color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# setup the color legend parameters for each legend in this view

# get color legend/bar for elevationLUT in view renderView1
elevationLUTColorBar = GetScalarBar(elevationLUT, renderView1)
elevationLUTColorBar.Title = 'Elevation'
elevationLUTColorBar.ComponentTitle = ''
elevationLUTColorBar.AutomaticLabelFormat = 0
elevationLUTColorBar.LabelFormat = '%.1f'
elevationLUTColorBar.NumberOfLabels = 10
elevationLUTColorBar.RangeLabelFormat = '%.1f'

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(transform1)
# ----------------------------------------------------------------