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
renderView1.ViewSize = [1160, 912]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.StereoType = 0
renderView1.CameraPosition = [3.76687547966054, 5.62637881722241, 4.44163730510425]
renderView1.CameraFocalPoint = [0.0241978424871666, -0.0474471125809167, 0.0405907851464954]
renderView1.CameraViewUp = [-0.384789750616684, -0.393723993522038, 0.834816305989173]
renderView1.CameraParallelScale = 1.73205080756888
renderView1.Background = [0.32, 0.34, 0.43]

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
scalarcsv = CSVReader(FileName=['Y:\\ParaView\\Data\\scalar.csv'])

# create a new 'Table To Structured Grid'
tableToStructuredGrid1 = TableToStructuredGrid(Input=scalarcsv)
tableToStructuredGrid1.WholeExtent = [0, 31, 0, 31, 0, 31]
tableToStructuredGrid1.XColumn = 'X32'
tableToStructuredGrid1.YColumn = 'Y32'
tableToStructuredGrid1.ZColumn = 'Z32'

# create a new 'Threshold'
threshold1 = Threshold(Input=tableToStructuredGrid1)
threshold1.Scalars = ['POINTS', 'S']
threshold1.ThresholdRange = [27.0336, 86.1696]
threshold1.UseContinuousCellRange = 1

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get color transfer function/color map for 'S'
sLUT = GetColorTransferFunction('S')
sLUT.RGBPoints = [0.0, 0.0, 0.0, 1.0, 168.96, 1.0, 0.0, 0.0]
sLUT.ColorSpace = 'HSV'
sLUT.NanColor = [0.498039215686, 0.498039215686, 0.498039215686]
sLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'S'
sPWF = GetOpacityTransferFunction('S')
sPWF.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]
sPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from tableToStructuredGrid1
tableToStructuredGrid1Display = Show(tableToStructuredGrid1, renderView1)
# trace defaults for the display properties.
tableToStructuredGrid1Display.Representation = '3D Glyphs'
tableToStructuredGrid1Display.ColorArrayName = ['POINTS', 'S']
tableToStructuredGrid1Display.LookupTable = sLUT
tableToStructuredGrid1Display.OSPRayScaleArray = 'S'
tableToStructuredGrid1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tableToStructuredGrid1Display.GlyphType = 'Sphere'
tableToStructuredGrid1Display.ScalarOpacityUnitDistance = 0.11174521339154

# init the 'Sphere' selected for 'GlyphType'
tableToStructuredGrid1Display.GlyphType.Radius = 0.01

# show color legend
tableToStructuredGrid1Display.SetScalarBarVisibility(renderView1, True)

# show data from threshold1
threshold1Display = Show(threshold1, renderView1)
# trace defaults for the display properties.
threshold1Display.Representation = '3D Glyphs'
threshold1Display.ColorArrayName = ['POINTS', 'S']
threshold1Display.LookupTable = sLUT
threshold1Display.OSPRayScaleArray = 'S'
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.GlyphType = 'Sphere'
threshold1Display.ScalarOpacityUnitDistance = 0.173035290251301
threshold1Display.SetScaleArray = ['POINTS', 'S']
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityArray = ['POINTS', 'S']
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'Sphere' selected for 'GlyphType'
threshold1Display.GlyphType.Radius = 0.01

# show color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# setup the color legend parameters for each legend in this view

# get color legend/bar for sLUT in view renderView1
sLUTColorBar = GetScalarBar(sLUT, renderView1)
sLUTColorBar.Title = 'S'
sLUTColorBar.ComponentTitle = ''
sLUTColorBar.AutomaticLabelFormat = 0
sLUTColorBar.LabelFormat = '%-#6.1f'
sLUTColorBar.NumberOfLabels = 10
sLUTColorBar.RangeLabelFormat = '%6.1f'

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(None)
# ----------------------------------------------------------------