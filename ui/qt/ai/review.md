# Review of the generated code

The three prompts in `prompts.md` were answered in one pass each, without
running anything. That output is kept unchanged in `generated/`. This file
records what happened when the code was run and tested, and what was changed
in the corrected versions in this folder.

## Starting point

The original `general/lecture4_notebook/gwflow.py` no longer runs in the course
environment: `calfem.vis` needs the `visvis` package, which is not installed.
The solver part runs fine; plotting was moved to `calfem.vis_mpl`.

## What worked

- The model class reproduced the original script exactly: 1307 nodes,
  1189 elements, heads 0 to 10 m, max element flow 0.9798.
- The worker thread pattern was correct: worker object, `moveToThread`,
  signals back to the GUI, inputs disabled while solving, `closeEvent` waits
  for the thread. Gmsh meshing works in the worker thread.
- `update_controls()` / `update_model()`, the dock with a `QFormLayout` and
  the qtpy imports followed the conventions asked for.
- Four of the five generated tests were meaningful physics checks and passed:
  prescribed heads, heads between the boundary values, inflow equals outflow
  (3.23 in both directions) and doubling the permeability doubles the flow.

## What was wrong

| # | Where | Problem | How it was found | Who is to blame |
|---|-------|---------|------------------|-----------------|
| 1 | UI | The flow plot was empty. `cfv.draw_element_values()` has no `axes` argument and draws on the current pyplot axes, so the plot went to a hidden pyplot figure (a new one on every redraw) and the embedded axes stayed blank. | Running the UI and looking at it | Generated code: wrong assumption about a library API |
| 2 | Model, UI | A notch deeper or wider than the region (`d > h`, `t > w`) makes Gmsh hang indefinitely. `d == h` fails with `IndexError`. The spin box ranges were set per field, but the valid ranges depend on each other. In the UI a hang would block the worker thread forever, and closing the window would wait forever. | Trying invalid input | Generated code: no validation |
| 3 | UI | Permeability used a spin box with range 0.01 to 100 m/s and two decimals. Real soils span about 1e-10 to 1e-2 m/s, which the spin box cannot represent. | Domain knowledge | Generated code: plausible-looking but unphysical ranges |
| 4 | Model | One-point integration (`ep = [1.0, 1]`) copied from the original. The element matrix has rank 2 instead of 3, which allows spurious hourglass modes. | A generated test failed (item 6), and the investigation led here | Original script; the AI copied it without question |
| 5 | Model, UI | "Max flow" was used as the summary value. The notch has re-entrant corners where the exact gradient is singular, so the maximum grows with mesh refinement (0.98, 1.13, 1.41 for size factors 1, 0.5, 0.25). Total flow converges (3.23). | Refining the mesh | Original script; the AI copied it |
| 6 | Tests | The antisymmetry test used a tolerance of 1e-6, but the Gmsh mesh is not symmetric, so the discrete solution is antisymmetric only to within the discretisation error (about 1e-2 m). The test would also have passed if no mirrored nodes were found. | Running the tests | Generated code: exact expectation for an approximate solution |

## Changes in the corrected versions

- `gwflow_model.py`: `validate()` called first in `solve()`; integration rule
  as an attribute `int_rule`, default 2; `total_flow` computed from the
  reaction flows; element coordinates `ex`, `ey` stored for plotting.
- `test_gwflow_model.py`: antisymmetry tolerance 0.2 % of the head
  difference and a check that pairs were found; total flow instead of max
  flow; new tests for the element matrix rank and for invalid geometry.
  10 tests, all passing.
- `gwflow_ui.py`: flow drawn with a `PolyCollection` on the embedded axes;
  colour bars; permeabilities as validated line edits in scientific notation;
  parameters validated in the GUI thread before the worker starts; total flow
  in the status bar.

With 2 x 2 integration the results differ from the original script: total
flow 3.2528 instead of 3.2271 at the default mesh.

## Not changed

- The GUI is only partly responsive while solving: in a test, a 50 ms timer
  fired 20 times during a 1.7 s solve instead of about 33. The assembly loop
  is pure Python and holds the GIL (Part 7). Vectorised assembly or a
  separate process would help.
- A running solve cannot be cancelled. With validation in place solves take
  seconds, so closing the window waits briefly at most.
