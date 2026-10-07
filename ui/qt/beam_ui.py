"""
Beam calculator. Shows how to separate the model (beam_model_decorators.py)
from the user interface using update_controls() and update_model().
"""

import sys

from qtpy.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QFormLayout, QVBoxLayout,
)
from qtpy.QtGui import QFontDatabase, QTextCursor

import beam_model_decorators as bm


class BeamWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """BeamWindow constructor"""
        super().__init__()

        # Create model instance

        self.beam = bm.BeamSimplySupported()

        # Configure window

        self.resize(500, 500)
        self.move(50, 50)
        self.setWindowTitle("Beam calculator")

        # Create controls

        self.a_edit = QLineEdit()
        self.b_edit = QLineEdit()
        self.P_edit = QLineEdit()
        self.E_edit = QLineEdit()
        self.I_edit = QLineEdit()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))

        # Layout. QFormLayout places labels and input fields in two columns.

        form = QFormLayout()
        form.addRow("a (m)", self.a_edit)
        form.addRow("b (m)", self.b_edit)
        form.addRow("P (N)", self.P_edit)
        form.addRow("E (Pa)", self.E_edit)
        form.addRow("I (m⁴)", self.I_edit)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.text_edit)

        # Connect signals to event methods

        self.a_edit.editingFinished.connect(self.on_editing_finished)
        self.b_edit.editingFinished.connect(self.on_editing_finished)
        self.P_edit.editingFinished.connect(self.on_editing_finished)
        self.E_edit.editingFinished.connect(self.on_editing_finished)
        self.I_edit.editingFinished.connect(self.on_editing_finished)

        # Fill controls with values from the model

        self.update_controls()

    def update_controls(self) -> None:
        """Model -> controls"""

        self.a_edit.setText(str(self.beam.a))
        self.b_edit.setText(str(self.beam.b))
        self.P_edit.setText(str(self.beam.P))
        self.E_edit.setText(str(self.beam.E))
        self.I_edit.setText(str(self.beam.I))

        self.update_text_edit()

    def update_text_edit(self) -> None:
        """Fill the text control with section values along the beam"""

        lines = [f"{'x (m)':>10}  {'v (m)':>10}  {'V (N)':>10}  {'M (Nm)':>10}"]

        for x in self.beam.x_values():
            lines.append(
                f"{x:10.5g}  {self.beam.v(x):10.5g}  {self.beam.V(x):10.5g}  {self.beam.M(x):10.5g}"
            )

        self.text_edit.setPlainText("\n".join(lines))
        self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)

    def update_model(self) -> None:
        """Controls -> model. Invalid values are ignored by the model."""

        self.beam.a = self.a_edit.text()
        self.beam.b = self.b_edit.text()
        self.beam.P = self.P_edit.text()
        self.beam.E = self.E_edit.text()
        self.beam.I = self.I_edit.text()

    def on_editing_finished(self) -> None:
        """Called when editing of any input field is finished"""

        # Read values from the controls, then write them back so that
        # invalid input is replaced with the value kept by the model.

        self.update_model()
        self.update_controls()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = BeamWindow()
    window.show()

    sys.exit(app.exec())
