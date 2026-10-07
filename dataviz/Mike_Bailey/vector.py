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
renderView1.ViewSize = [1107, 981]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [0.5524948266165699, 0.1628749699399068, -0.2654437053760541]
renderView1.StereoType = 0
renderView1.CameraPosition = [2.96871077423869, 1.807450280058381, 4.398004570489099]
renderView1.CameraFocalPoint = [0.10461048819091585, -0.05284362036731993, 0.1290525637039153]
renderView1.CameraViewUp = [0.0354881223603353, 0.9072220812129917, -0.41915234525278033]
renderView1.CameraParallelScale = 0.307935405212305
renderView1.Background = [0.32, 0.34, 0.43]

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
vectorcsv = CSVReader(FileName=['Y:\\ParaView\\Data\\vector.csv'])

# create a new 'Table To Structured Grid'
tableToStructuredGrid1 = TableToStructuredGrid(Input=vectorcsv)
tableToStructuredGrid1.WholeExtent = [0, 31, 0, 31, 0, 31]
tableToStructuredGrid1.XColumn = 'X32'
tableToStructuredGrid1.YColumn = 'Y32'
tableToStructuredGrid1.ZColumn = 'Z32'

# create a new 'Calculator'
calculator1 = Calculator(Input=tableToStructuredGrid1)
calculator1.ResultArrayName = 'V'
calculator1.Function = 'Vx*iHat+Vy*jHat+Vz*kHat'

# create a new 'Calculator'
calculator2 = Calculator(Input=calculator1)
calculator2.ResultArrayName = 'Mag'
calculator2.Function = 'mag(V)'

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(Input=calculator2,
    SeedType='Point Source')
streamTracer1.Vectors = ['POINTS', 'V']
streamTracer1.MaximumStreamlineLength = 2.0

# init the 'Point Source' selected for 'SeedType'
streamTracer1.SeedType.Center = [0.188790836058341, 0.224398949853218, 0.468613366625134]
streamTracer1.SeedType.NumberOfPoints = 200

# create a new 'Tube'
tube1 = Tube(Input=streamTracer1)
tube1.Scalars = ['POINTS', 'Mag']
tube1.Vectors = ['POINTS', 'Normals']
tube1.Radius = 0.013589609432220462

# create a new 'Glyph'
glyph1 = Glyph(Input=calculator2,
    GlyphType='Arrow')
glyph1.Scalars = ['POINTS', 'Mag']
glyph1.Vectors = ['POINTS', 'V']
glyph1.ScaleMode = 'scalar'
glyph1.ScaleFactor = 0.126
glyph1.GlyphTransform = 'Transform2'

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get color transfer function/color map for 'V'
vLUT = GetColorTransferFunction('V')
vLUT.RGBPoints = [0.0, 0.0, 0.0, 1.0, 3.46410161513775, 1.0, 0.0, 0.0]
vLUT.ColorSpace = 'HSV'
vLUT.NanColor = [0.498039215686, 0.498039215686, 0.498039215686]
vLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'V'
vPWF = GetOpacityTransferFunction('V')
vPWF.Points = [0.0, 0.0, 0.5, 0.0, 3.46410161513775, 1.0, 0.5, 0.0]
vPWF.ScalarRangeInitialized = 1

# get color transfer function/color map for 'Mag'
magLUT = GetColorTransferFunction('Mag')
magLUT.RGBPoints = [0.0, 0.0, 0.0, 1.0, 3.46410161513776, 1.0, 0.0, 0.0]
magLUT.ColorSpace = 'HSV'
magLUT.NanColor = [0.498039215686, 0.498039215686, 0.498039215686]
magLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'Mag'
magPWF = GetOpacityTransferFunction('Mag')
magPWF.Points = [0.0, 0.0, 0.5, 0.0, 3.46410161513776, 1.0, 0.5, 0.0]
magPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from tableToStructuredGrid1
tableToStructuredGrid1Display = Show(tableToStructuredGrid1, renderView1)
# trace defaults for the display properties.
tableToStructuredGrid1Display.Representation = 'Outline'
tableToStructuredGrid1Display.ColorArrayName = [None, '']
tableToStructuredGrid1Display.OSPRayScaleArray = 'Vx'
tableToStructuredGrid1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tableToStructuredGrid1Display.GlyphType = 'Arrow'
tableToStructuredGrid1Display.ScalarOpacityUnitDistance = 0.11174521339154

# show data from calculator1
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = '3D Glyphs'
calculator1Display.ColorArrayName = ['POINTS', 'V']
calculator1Display.LookupTable = vLUT
calculator1Display.Opacity = 0.81
calculator1Display.OSPRayScaleArray = 'Vx'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.ScalarOpacityUnitDistance = 0.11174521339154

# init the 'Arrow' selected for 'GlyphType'
calculator1Display.GlyphType.TipRadius = 0.0
calculator1Display.GlyphType.TipLength = 0.11
calculator1Display.GlyphType.ShaftRadius = 0.1

# show data from calculator2
calculator2Display = Show(calculator2, renderView1)
# trace defaults for the display properties.
calculator2Display.Representation = 'Outline'
calculator2Display.ColorArrayName = ['POINTS', 'Mag']
calculator2Display.LookupTable = magLUT
calculator2Display.Specular = 0.92
calculator2Display.OSPRayScaleArray = 'Mag'
calculator2Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator2Display.GlyphType = 'Arrow'
calculator2Display.ScalarOpacityUnitDistance = 0.11174521339154

# show color legend
calculator2Display.SetScalarBarVisibility(renderView1, True)

# show data from glyph1
glyph1Display = Show(glyph1, renderView1)
# trace defaults for the display properties.
glyph1Display.ColorArrayName = ['POINTS', 'Mag']
glyph1Display.LookupTable = magLUT
glyph1Display.OSPRayScaleArray = 'Mag'
glyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
glyph1Display.GlyphType = 'Arrow'
glyph1Display.SetScaleArray = ['POINTS', 'Mag']
glyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
glyph1Display.OpacityArray = ['POINTS', 'Mag']
glyph1Display.OpacityTransferFunction = 'PiecewiseFunction'

# show color legend
glyph1Display.SetScalarBarVisibility(renderView1, True)

# show data from streamTracer1
streamTracer1Display = Show(streamTracer1, renderView1)
# trace defaults for the display properties.
streamTracer1Display.ColorArrayName = ['POINTS', 'Mag']
streamTracer1Display.LookupTable = magLUT
streamTracer1Display.OSPRayScaleArray = 'Mag'
streamTracer1Display.OSPRayScaleFunction = 'PiecewiseFunction'
streamTracer1Display.GlyphType = 'Arrow'
streamTracer1Display.ShaderPreset = 'Gaussian Blur (Default)'
streamTracer1Display.SetScaleArray = ['POINTS', 'Mag']
streamTracer1Display.ScaleTransferFunction = 'PiecewiseFunction'
streamTracer1Display.OpacityArray = ['POINTS', 'Mag']
streamTracer1Display.OpacityTransferFunction = 'PiecewiseFunction'

# show color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# show data from tube1
tube1Display = Show(tube1, renderView1)
# trace defaults for the display properties.
tube1Display.ColorArrayName = ['POINTS', 'Mag']
tube1Display.LookupTable = magLUT
tube1Display.Specular = 1.0
tube1Display.OSPRayScaleArray = 'Mag'
tube1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tube1Display.GlyphType = 'Arrow'
tube1Display.SetScaleArray = ['POINTS', 'Mag']
tube1Display.ScaleTransferFunction = 'PiecewiseFunction'
tube1Display.OpacityArray = ['POINTS', 'Mag']
tube1Display.OpacityTransferFunction = 'PiecewiseFunction'

# show color legend
tube1Display.SetScalarBarVisibility(renderView1, True)

# setup the color legend parameters for each legend in this view

# get color legend/bar for vLUT in view renderView1
vLUTColorBar = GetScalarBar(vLUT, renderView1)
vLUTColorBar.Title = 'V'
vLUTColorBar.ComponentTitle = 'Magnitude'

# get color legend/bar for magLUT in view renderView1
magLUTColorBar = GetScalarBar(magLUT, renderView1)
magLUTColorBar.Position = [0.85, 0.52]
magLUTColorBar.Title = 'Mag'
magLUTColorBar.ComponentTitle = ''

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(tube1)
# ----------------------------------------------------------------