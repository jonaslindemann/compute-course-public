# state file generated using paraview version 6.1.1
import paraview
paraview.compatibility.major = 6
paraview.compatibility.minor = 1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.Set(
    ViewSize=[2232, 1538],
    CenterOfRotation=[1.5544350147247314, 0.0, 0.7690349817276001],
    CameraPosition=[3.5015196795201784, 2.435215421029818, -2.040538021460471],
    CameraFocalPoint=[-0.08681190226540833, -2.0527046790704975, 3.1372951364680044],
    CameraViewUp=[-0.2691561207839282, 0.812252402996972, 0.5174949434247569],
)

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(2232, 1538)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'Legacy VTK Reader'
uvwvtk = LegacyVTKReader(registrationName='uvw.vtk', FileNames=['C:\\users\\jonas lindemann\\Development\\compute-course-public\\dataviz\\uvw.vtk'])

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=uvwvtk,
    SeedType='Point Cloud')
streamTracer1.Set(
    Vectors=['POINTS', 'vec1'],
    MaximumStreamlineLength=3.108870029449463,
)

# init the 'Point Cloud' selected for 'SeedType'
streamTracer1.SeedType.Set(
    Center=[1.5544350147247314, 0.0, 0.7690349817276001],
    NumberOfPoints=500,
    Radius=1.5,
)

# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=uvwvtk,
    GlyphType='Line')
glyph1.Set(
    OrientationArray=['POINTS', 'vec1'],
    ScaleArray=['POINTS', 'vec1'],
    ScaleFactor=0.13057254123687745,
)

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from uvwvtk
uvwvtkDisplay = Show(uvwvtk, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
uvwvtkDisplay.Set(
    Representation='Surface',
    ColorArrayName=['POINTS', ''],
    Opacity=0.13,
)

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
uvwvtkDisplay.ScaleTransferFunction.Points = [-0.00010851999832084402, 0.0, 0.5, 0.0, 0.8231620192527771, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
uvwvtkDisplay.OpacityTransferFunction.Points = [-0.00010851999832084402, 0.0, 0.5, 0.0, 0.8231620192527771, 1.0, 0.5, 0.0]

# show data from streamTracer1
streamTracer1Display = Show(streamTracer1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'vec1'
vec1LUT = GetColorTransferFunction('vec1')
vec1LUT.Set(
    RGBPoints=GenerateRGBPoints(
        range_min=1.3773731486481578e-06,
        range_max=0.8236047875924813,
    ),
    ScalarRangeInitialized=1.0,
)

# trace defaults for the display properties.
streamTracer1Display.Set(
    Representation='Surface',
    ColorArrayName=['POINTS', 'vec1'],
    LookupTable=vec1LUT,
)

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
streamTracer1Display.ScaleTransferFunction.Points = [-2.667933385419605, 0.0, 0.5, 0.0, 3.2171294562419708, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
streamTracer1Display.OpacityTransferFunction.Points = [-2.667933385419605, 0.0, 0.5, 0.0, 3.2171294562419708, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for vec1LUT in view renderView1
vec1LUTColorBar = GetScalarBar(vec1LUT, renderView1)
vec1LUTColorBar.Set(
    Title='vec1',
    ComponentTitle='Magnitude',
)

# set color bar visibility
vec1LUTColorBar.Visibility = 1

# show color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity maps used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'vec1'
vec1PWF = GetOpacityTransferFunction('vec1')
vec1PWF.Set(
    Points=[1.3773731486481578e-06, 0.0, 0.5, 0.0, 0.8236047875924813, 1.0, 0.5, 0.0],
    ScalarRangeInitialized=1,
)

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
animationScene1.Set(
    ViewModules=renderView1,
    Cues=timeAnimationCue1,
    AnimationTime=0.0,
)

# initialize the animation scene

# ----------------------------------------------------------------
# restore active source
SetActiveSource(streamTracer1)
# ----------------------------------------------------------------


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
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
## https://www.paraview.org/paraview-docs/nightly/python/
##--------------------------------------------