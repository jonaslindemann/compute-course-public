# state file generated using paraview version 5.13.2
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1758, 1146]
renderView1.AxesGrid = 'Grid Axes 3D Actor'
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [3.7741022079965734, 2.3382787650832126, 4.888999550916191]
renderView1.CameraFocalPoint = [-0.2890663841839072, -0.10035001372051033, 0.16371010353467877]
renderView1.CameraViewUp = [-0.11389394324510861, 0.9193741150270595, -0.37653606243000304]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 1.7320508075688772
renderView1.LegendGrid = 'Legend Grid Actor'
renderView1.PolarGrid = 'Polar Grid Actor'
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# init the 'Grid Axes 3D Actor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1758, 1146)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
scalarcsv = CSVReader(registrationName='scalar.csv', FileName=['c:\\users\\Jonas Lindemann\\Development\\paraview-workshop\\Mike_Bailey\\Examples\\scalar.csv'])

# create a new 'Table To Structured Grid'
tableToStructuredGrid1 = TableToStructuredGrid(registrationName='TableToStructuredGrid1', Input=scalarcsv)
tableToStructuredGrid1.WholeExtent = [0, 31, 0, 31, 0, 31]
tableToStructuredGrid1.XColumn = 'X32'
tableToStructuredGrid1.YColumn = 'Y32'
tableToStructuredGrid1.ZColumn = 'Z32'

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=tableToStructuredGrid1)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['POINTS', 'S']
clip1.Value = 84.48

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from tableToStructuredGrid1
tableToStructuredGrid1Display = Show(tableToStructuredGrid1, renderView1, 'StructuredGridRepresentation')

# get 2D transfer function for 'S'
sTF2D = GetTransferFunction2D('S')

# get color transfer function/color map for 'S'
sLUT = GetColorTransferFunction('S')
sLUT.TransferFunction2D = sTF2D
sLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 84.48, 0.865003, 0.865003, 0.865003, 168.96, 0.705882, 0.0156863, 0.14902]
sLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'S'
sPWF = GetOpacityTransferFunction('S')
sPWF.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]
sPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
tableToStructuredGrid1Display.Representation = 'Surface'
tableToStructuredGrid1Display.ColorArrayName = ['POINTS', 'S']
tableToStructuredGrid1Display.LookupTable = sLUT
tableToStructuredGrid1Display.Opacity = 0.5
tableToStructuredGrid1Display.SelectNormalArray = 'None'
tableToStructuredGrid1Display.SelectTangentArray = 'None'
tableToStructuredGrid1Display.SelectTCoordArray = 'None'
tableToStructuredGrid1Display.TextureTransform = 'Transform2'
tableToStructuredGrid1Display.OSPRayScaleArray = 'S'
tableToStructuredGrid1Display.OSPRayScaleFunction = 'Piecewise Function'
tableToStructuredGrid1Display.Assembly = ''
tableToStructuredGrid1Display.SelectedBlockSelectors = ['']
tableToStructuredGrid1Display.SelectOrientationVectors = 'None'
tableToStructuredGrid1Display.ScaleFactor = 0.2
tableToStructuredGrid1Display.SelectScaleArray = 'None'
tableToStructuredGrid1Display.GlyphType = 'Arrow'
tableToStructuredGrid1Display.GlyphTableIndexArray = 'None'
tableToStructuredGrid1Display.GaussianRadius = 0.01
tableToStructuredGrid1Display.SetScaleArray = ['POINTS', 'S']
tableToStructuredGrid1Display.ScaleTransferFunction = 'Piecewise Function'
tableToStructuredGrid1Display.OpacityArray = ['POINTS', 'S']
tableToStructuredGrid1Display.OpacityTransferFunction = 'Piecewise Function'
tableToStructuredGrid1Display.DataAxesGrid = 'Grid Axes Representation'
tableToStructuredGrid1Display.PolarAxes = 'Polar Axes Representation'
tableToStructuredGrid1Display.ScalarOpacityFunction = sPWF
tableToStructuredGrid1Display.ScalarOpacityUnitDistance = 0.11174521339154046
tableToStructuredGrid1Display.SelectInputVectors = [None, '']
tableToStructuredGrid1Display.WriteLog = ''

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
tableToStructuredGrid1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
tableToStructuredGrid1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]

# show data from clip1
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['POINTS', 'S']
clip1Display.LookupTable = sLUT
clip1Display.SelectNormalArray = 'None'
clip1Display.SelectTangentArray = 'None'
clip1Display.SelectTCoordArray = 'None'
clip1Display.TextureTransform = 'Transform2'
clip1Display.OSPRayScaleArray = 'S'
clip1Display.OSPRayScaleFunction = 'Piecewise Function'
clip1Display.Assembly = ''
clip1Display.SelectedBlockSelectors = ['']
clip1Display.SelectOrientationVectors = 'None'
clip1Display.ScaleFactor = 0.2
clip1Display.SelectScaleArray = 'None'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'None'
clip1Display.GaussianRadius = 0.01
clip1Display.SetScaleArray = ['POINTS', 'S']
clip1Display.ScaleTransferFunction = 'Piecewise Function'
clip1Display.OpacityArray = ['POINTS', 'S']
clip1Display.OpacityTransferFunction = 'Piecewise Function'
clip1Display.DataAxesGrid = 'Grid Axes Representation'
clip1Display.PolarAxes = 'Polar Axes Representation'
clip1Display.ScalarOpacityFunction = sPWF
clip1Display.ScalarOpacityUnitDistance = 0.12064429723158014
clip1Display.OpacityArrayName = ['POINTS', 'S']
clip1Display.SelectInputVectors = [None, '']
clip1Display.WriteLog = ''

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
clip1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
clip1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 168.96, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for sLUT in view renderView1
sLUTColorBar = GetScalarBar(sLUT, renderView1)
sLUTColorBar.Title = 'S'
sLUTColorBar.ComponentTitle = ''

# set color bar visibility
sLUTColorBar.Visibility = 1

# show color legend
tableToStructuredGrid1Display.SetScalarBarVisibility(renderView1, True)

# show color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity maps used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup animation scene, tracks and keyframes
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# initialize the timekeeper

# get time animation track
timeAnimationCue1 = GetTimeTrack()

# initialize the animation track

# get animation scene
animationScene1 = GetAnimationScene()

# initialize the animation scene
animationScene1.ViewModules = renderView1
animationScene1.Cues = timeAnimationCue1
animationScene1.AnimationTime = 0.0

# initialize the animation scene

# ----------------------------------------------------------------
# restore active source
SetActiveSource(tableToStructuredGrid1)
# ----------------------------------------------------------------


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
#RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
Interact()
#
## Save a screenshot of the active view
#SaveScreenshot("myvectors.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://www.paraview.org/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------