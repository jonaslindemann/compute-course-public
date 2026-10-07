"""
Tests for GroundwaterModel. Run with:

    pytest test_gwflow_model.py
"""

import numpy as np
import pytest

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

    assert inflow == pytest.approx(-outflow, rel=1e-6)


def test_antisymmetric_about_centre_line(model):
    # With the notch centred, head(x, y) + head(w - x, y) = head_left + head_right

    coords = model.coords
    mirrored = coords.copy()
    mirrored[:, 0] = model.w - coords[:, 0]

    total = model.head_left + model.head_right

    for i, p in enumerate(mirrored):
        dist = np.linalg.norm(coords - p, axis=1)
        j = np.argmin(dist)
        if dist[j] < 1e-6:
            assert model.a[i] + model.a[j] == pytest.approx(total, abs=1e-6)


def test_double_permeability_doubles_flow(model):
    stiff = GroundwaterModel()
    stiff.kx = 2.0 * model.kx
    stiff.ky = 2.0 * model.ky
    stiff.solve()

    assert stiff.flow.max() == pytest.approx(2.0 * model.flow.max(), rel=1e-6)
