# Prompts used to create the groundwater flow application

The starting point is `general/lecture4_notebook/gwflow.py`, a CALFEM script
with hard-coded parameters that solves, then opens four plot windows.

The code produced by each prompt is kept unchanged in `generated/`.
The tested and corrected versions are in this folder. `review.md` lists
every change and why it was needed.

## Prompt 1: extract a model

> Here is gwflow.py, a CALFEM script that computes 2D groundwater flow
> [script pasted]. Refactor it into a module gwflow_model.py with a class
> GroundwaterModel.
>
> - Geometry, permeabilities, the two boundary heads and the element size
>   factor should be attributes, with the values from the script as defaults.
> - A method solve() that creates the geometry and mesh, assembles and solves
>   the system, and stores the coordinates, topology, nodal heads and element
>   flow magnitudes as attributes.
> - No plotting and no Qt imports. Plot with calfem.vis_mpl elsewhere.
> - Keep a `__main__` block that solves and prints a short summary.

## Prompt 2: tests

> Write pytest tests for GroundwaterModel in test_gwflow_model.py. Test the
> physics, not only that the code runs:
>
> - the prescribed heads are enforced on the boundaries,
> - all heads lie between the two boundary values,
> - inflow equals outflow,
> - the solution is antisymmetric about the centre line when the notch is
>   centred,
> - doubling the permeability doubles the flow.

## Prompt 3: user interface

> Write gwflow_ui.py, a Qt user interface for GroundwaterModel. Import Qt
> through qtpy and use the Qt 6 API. Follow these conventions:
>
> - A QMainWindow with the parameters in a dock: a QFormLayout of
>   QDoubleSpinBoxes with sensible ranges and units.
> - update_controls() copies the model to the controls, update_model() copies
>   the controls to the model.
> - A Solve button runs model.solve() in a worker object in a QThread so the
>   window stays responsive. Show that it is busy and disable the inputs while
>   solving.
> - Show the head distribution or the flow magnitude, selected with a combo
>   box, using calfem.vis_mpl in an embedded matplotlib FigureCanvasQTAgg with
>   a navigation toolbar.
