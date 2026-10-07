"""
Tests for GroundwaterModel. Run with:

    pytest test_gwflow_model.py

Corrected version of generated/test_gwflow_model.py. See review.md.
"""

import numpy as np
import pytest

import calfem.core as cfc

from gwflow_model import GroundwaterModel


@pytest.fixture(scope="module")
def model():
    """A solved model with default parameters. Solved once for all tests."""
    m = GroundwaterModel()
    m.solve()
    return m


def boundary_dofs(model, marker):
    """Zero based indices of the dofs on a marked boundary"""
    return np.array(model.bdofs[marker]) - 1


def test_prescribed_heads_are_enforced(model):
    left = boundary_dofs(model, GroundwaterModel.LEFT_MARKER)
    right = boundary_dofs(model, GroundwaterModel.RIGHT_MARKER)

    assert np.allclose(model.a[left], model.head_left)
    assert np.allclose(model.a[right], model.head_right)


def test_heads_between_boundary_values(model):
    lo = min(model.head_left, model.head_right)
    hi = max(model.head_left, model.head_right)

    assert model.a.min() >= lo - 1e-9
    assert model.a.max() <= hi + 1e-9


def test_inflow_equals_outflow(model):
    left = boundary_dofs(model, GroundwaterModel.LEFT_MARKER)
    right = boundary_dofs(model, GroundwaterModel.RIGHT_MARKER)

    inflow = model.r[left].sum()
    outflow = model.r[right].sum()

    assert inflow > 0.0
    assert inflow == pytest.approx(-outflow, rel=1e-6)


def test_antisymmetric_about_centre_line(model):
    # With the notch centred, head(x, y) + head(w - x, y) = head_left + head_right
    # for the exact solution. The Gmsh mesh is not symmetric, so the discrete
    # solution only satisfies this to within the discretisation error. The
    # tolerance is 0.2 % of the head difference.

    coords = model.coords
    mirrored = coords.copy()
    mirrored[:, 0] = model.w - coords[:, 0]

    total = model.head_left + model.head_right
    tol = 0.002 * abs(model.head_left - model.head_right)

    errors = []

    for i, p in enumerate(mirrored):
        dist = np.linalg.norm(coords - p, axis=1)
        j = np.argmin(dist)
        if dist[j] < 1e-6:
            errors.append(abs(model.a[i, 0] + model.a[j, 0] - total))

    # Make sure the test actually compared something

    assert len(errors) > 50
    assert max(errors) < tol


def test_double_permeability_doubles_flow(model):
    stiff = GroundwaterModel()
    stiff.kx = 2.0 * model.kx
    stiff.ky = 2.0 * model.ky
    stiff.solve()

    assert stiff.total_flow == pytest.approx(2.0 * model.total_flow, rel=1e-6)


def test_element_matrix_has_full_rank(model):
    # A 4-node flow element has exactly one zero-energy mode: constant head.
    # One-point integration gives rank 2 and spurious hourglass modes.

    ex = np.array([0.0, 1.0, 1.0, 0.0])
    ey = np.array([0.0, 0.0, 1.0, 1.0])
    Ke = cfc.flw2i4e(ex, ey, [1.0, model.int_rule], np.eye(2))

    assert np.linalg.matrix_rank(Ke) == 3


@pytest.mark.parametrize("name, value", [("d", 10.0), ("d", 12.0), ("t", 100.0), ("t", 150.0)])
def test_invalid_geometry_is_rejected(name, value):
    # Without validation these cases hang in Gmsh or fail with an IndexError

    m = GroundwaterModel()
    setattr(m, name, value)

    with pytest.raises(ValueError):
        m.solve()
