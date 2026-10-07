"""
Numeric input: QSpinBox, QDoubleSpinBox and QLineEdit with a QDoubleValidator.

Spin boxes can never contain an invalid value, so no conversion or error
handling is needed. A validated QLineEdit is better for values spanning
many orders of magnitude, such as Young's modulus, where scientific
notation is convenient.

The example computes the tip deflection of a cantilever beam,
delta = P L^3 / (3 E I), and updates the result as soon as an input changes.
"""

import sys

from qtpy.QtWidgets import (
    QApplication, QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QLabel,
    QFormLayout, QVBoxLayout,
)
from qtpy.QtGui import QDoubleValidator
from qtpy.QtCore import QLocale


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.move(50, 50)
        self.setWindowTitle("Numeric input")

        # QDoubleSpinBox: range, step, decimals and unit suffix

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.1, 20.0)
        self.length_spin.setSingleStep(0.1)
        self.length_spin.setDecimals(2)
        self.length_spin.setSuffix(" m")
        self.length_spin.setValue(3.0)

        self.load_spin = QDoubleSpinBox()
        self.load_spin.setRange(0.0, 1e6)
        self.load_spin.setSingleStep(100.0)
        self.load_spin.setDecimals(1)
        self.load_spin.setSuffix(" N")
        self.load_spin.setValue(1000.0)

        # QLineEdit with a validator. The C locale makes "2.1e11" valid
        # also on systems using a decimal comma, such as Swedish Windows.

        validator = QDoubleValidator(1e-12, 1e15, 6, self)
        validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        validator.setLocale(QLocale.c())

        self.E_edit = QLineEdit("2.1e11")
        self.E_edit.setValidator(validator)

        self.I_edit = QLineEdit("8.33e-6")
        self.I_edit.setValidator(validator)

        # QSpinBox: integers only

        self.decimals_spin = QSpinBox()
        self.decimals_spin.setRange(1, 10)
        self.decimals_spin.setValue(4)

        self.result_label = QLabel()

        # Layout

        form = QFormLayout()
        form.addRow("Length L", self.length_spin)
        form.addRow("Load P", self.load_spin)
        form.addRow("E (Pa)", self.E_edit)
        form.addRow("I (m⁴)", self.I_edit)
        form.addRow("Significant digits", self.decimals_spin)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.result_label)
        layout.addStretch()

        # Connect signals. valueChanged/textChanged give immediate updates.

        self.length_spin.valueChanged.connect(self.update_result)
        self.load_spin.valueChanged.connect(self.update_result)
        self.decimals_spin.valueChanged.connect(self.update_result)
        self.E_edit.textChanged.connect(self.update_result)
        self.I_edit.textChanged.connect(self.update_result)

        self.update_result()

    def update_result(self):
        """Compute and show the tip deflection"""

        # hasAcceptableInput() is False while the user is typing an
        # incomplete number such as "2.1e"

        valid = True

        for edit in (self.E_edit, self.I_edit):
            ok = edit.hasAcceptableInput()
            edit.setStyleSheet("" if ok else "background-color: #f8d7da;")
            valid = valid and ok

        if not valid:
            self.result_label.setText("Tip deflection: (invalid input)")
            return

        L = self.length_spin.value()
        P = self.load_spin.value()
        E = float(self.E_edit.text())
        I = float(self.I_edit.text())

        delta = P * L**3 / (3 * E * I)

        digits = self.decimals_spin.value()
        self.result_label.setText(f"Tip deflection: {delta:.{digits}g} m")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
