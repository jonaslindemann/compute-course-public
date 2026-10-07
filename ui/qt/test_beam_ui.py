"""
Tests for the beam user interface. The window is created but never shown,
and user input is simulated by setting text and calling the slot.

Run with:

    pytest test_beam_ui.py

The pytest-qt plugin (qtbot fixture) can also simulate key presses and
mouse clicks, but is not needed for simple tests like these.
"""

import sys

from qtpy.QtWidgets import QApplication

import beam_ui

# A QApplication must exist before any widget is created

app = QApplication.instance() or QApplication(sys.argv)


def test_controls_show_model_values():
    window = beam_ui.BeamWindow()
    assert float(window.a_edit.text()) == window.beam.a
    assert float(window.I_edit.text()) == window.beam.I


def test_editing_updates_model():
    window = beam_ui.BeamWindow()
    window.b_edit.setText("5.0")
    window.on_editing_finished()
    assert window.beam.b == 5.0
    assert window.beam.L == window.beam.a + 5.0


def test_invalid_input_is_reverted():
    window = beam_ui.BeamWindow()
    old_P = window.beam.P
    window.P_edit.setText("abc")
    window.on_editing_finished()
    assert window.beam.P == old_P
    assert window.P_edit.text() == str(old_P)


def test_results_table_is_filled():
    window = beam_ui.BeamWindow()
    lines = window.text_edit.toPlainText().splitlines()
    assert lines[0].split()[0] == "x"
    assert len(lines) == 1 + len(window.beam.x_values())
