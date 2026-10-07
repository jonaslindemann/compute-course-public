"""
Tests for the beam model. Because the model has no user interface code,
it can be tested without creating any windows.

Run with:

    pytest test_beam_model.py
"""

from math import isclose

import beam_model_decorators as bm


def make_beam(a=1.0, b=2.0, P=1000.0, E=2.1e11, I=8.33e-6):
    """Create a beam with the given properties"""
    beam = bm.BeamSimplySupported()
    beam.a, beam.b, beam.P, beam.E, beam.I = a, b, P, E, I
    return beam


def test_length_follows_a_and_b():
    beam = make_beam(a=1.0, b=2.0)
    beam.b = 5.0
    assert beam.L == 6.0


def test_supports_have_zero_deflection():
    beam = make_beam()
    assert isclose(beam.v(0.0), 0.0, abs_tol=1e-12)
    assert isclose(beam.v(beam.L), 0.0, abs_tol=1e-12)


def test_midspan_deflection_matches_handbook():
    # Load at midspan: v_max = P L^3 / (48 E I)
    beam = make_beam(a=2.0, b=2.0)
    expected = beam.P * beam.L**3 / (48 * beam.E * beam.I)
    assert isclose(beam.v(beam.L / 2), expected, rel_tol=1e-9)


def test_shear_force_jumps_by_P_at_load():
    beam = make_beam(a=1.0, b=2.0)
    assert isclose(beam.V(0.999) - beam.V(1.001), beam.P)


def test_reactions_balance_load():
    beam = make_beam(a=1.0, b=2.0)
    left_reaction = beam.V(0.0)
    right_reaction = -beam.V(beam.L)
    assert isclose(left_reaction + right_reaction, beam.P)


def test_moment_is_continuous_and_largest_at_load():
    beam = make_beam(a=1.0, b=2.0)
    assert isclose(beam.M(0.999999), beam.M(1.0), rel_tol=1e-5)
    assert isclose(beam.M(1.0), -beam.P * beam.a * beam.b / beam.L)


def test_invalid_input_keeps_old_value():
    beam = make_beam(a=1.0)
    beam.a = "not a number"
    beam.a = None
    assert beam.a == 1.0


def test_string_input_is_converted():
    beam = make_beam()
    beam.P = "2500"
    assert beam.P == 2500.0


def test_x_values_cover_whole_beam():
    beam = make_beam(a=1.0, b=2.0)
    xs = beam.x_values(30)
    assert len(xs) == 31
    assert xs[0] == 0.0
    assert isclose(xs[-1], beam.L)
