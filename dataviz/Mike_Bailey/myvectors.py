# state file generated using paraview version 6.1.0
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
    ViewSize=[1706, 1142],
    CameraPosition=[1.4859073647853207, 3.20179626890755, 5.685524570918064],
    CameraViewUp=[-0.16165358645651093, 0.8773386234710063, -0.45182414471976506],
)

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1706, 1142)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
vectorcsv = CSVReader(registrationName='vector.csv', FileName=['C:\\Users\\Jonas Lindemann\\Development\\paraview-workshop\\Mike_Bailey\\Examples\\vector.csv'])

# create a new 'Table To Structured Grid'
tableToStructuredGrid1 = TableToStructuredGrid(registrationName='TableToStructuredGrid1', Input=vectorcsv)
tableToStructuredGrid1.Set(
    Dimensions=[32, 32, 32],
    XColumn='X32',
    YColumn='Y32',
    ZColumn='Z32',
)

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=tableToStructuredGrid1)
calculator1.Set(
    ResultArrayName='V',
    Function='Vx*iHat+Vy*jHat+Vz*kHat',
)

# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=calculator1,
    GlyphType='Arrow')
glyph1.Set(
    OrientationArray=['POINTS', 'V'],
    ScaleArray=['POINTS', 'V'],
    ScaleFactor=0.2,
)

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from calculator1
calculator1Display = Show(calculator1, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Set(
    Representation='Outline',
    ColorArrayName=[None, ''],
)

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [-2.0, 0.0, 0.5, 0.0, 2.0, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [-2.0, 0.0, 0.5, 0.0, 2.0, 1.0, 0.5, 0.0]

# show data from glyph1
glyph1Display = Show(glyph1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'V'
vLUT = GetColorTransferFunction('V')
vLUT.Set(
    RGBPoints=GenerateRGBPoints(
        range_min=0.0,
        range_max=3.181980515339464,
    ),
    ScalarRangeInitialized=1.0,
)

# trace defaults for the display properties.
glyph1Display.Set(
    Representation='Surface',
    ColorArrayName=['POINTS', 'V'],
    LookupTable=vLUT,
)

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
glyph1Display.ScaleTransferFunction.Points = [-2.0, 0.0, 0.5, 0.0, 1.75, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
glyph1Display.OpacityTransferFunction.Points = [-2.0, 0.0, 0.5, 0.0, 1.75, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for vLUT in view renderView1
vLUTColorBar = GetScalarBar(vLUT, renderView1)
vLUTColorBar.Set(
    Title='V',
    ComponentTitle='Magnitude',
)

# set color bar visibility
vLUTColorBar.Visibility = 1

# show color legend
glyph1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity maps used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'V'
vPWF = GetOpacityTransferFunction('V')
vPWF.Set(
    Points=[0.0, 0.0, 0.5, 0.0, 3.181980515339464, 1.0, 0.5, 0.0],
    ScalarRangeInitialized=1,
)

# ----------------------------------------------------------------
# setup animation scene, tracks and keyframes
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get time animation track
timeAnimationCue1 = GetTimeTrack()

# initialize the animation scene

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# initialize the timekeeper

# initialize the animation track

# get animation scene
animationScene1 = GetAnimationScene()

# initialize the animation scene
animationScene1.Set(
    ViewModules=renderView1,
    Cues=timeAnimationCue1,
    AnimationTime=0.0,
)

# ----------------------------------------------------------------
# restore active source
SetActiveSource(glyph1)
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
SaveScreenshot("myvectors.png")
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