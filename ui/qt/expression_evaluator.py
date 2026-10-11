"""
A small calculator that evaluates mathematical expressions.

Only names from the math module are available in the expression.
eval() is still not safe for untrusted input, but this keeps the
example from exposing builtins such as open() or __import__().
"""

import sys
import math

from qtpy.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
)

MATH_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}


class ExprEvalWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Size and position window

        self.resize(400, 120)
        self.move(50, 50)
        self.setWindowTitle("Expression calculator")

        # Create controls

        self.expression_edit = QLineEdit()
        self.expression_edit.setPlaceholderText("e.g. sin(pi/4)**2 + sqrt(2)")
        self.result_edit = QLineEdit()
        self.result_edit.setReadOnly(True)

        self.calc_button = QPushButton("Evaluate")
        self.calc_button.setDefault(True)
        self.close_button = QPushButton("Close")

        # Layout

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.calc_button)
        button_row.addWidget(self.close_button)
        button_row.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(self.expression_edit)
        layout.addWidget(self.result_edit)
        layout.addStretch()
        layout.addLayout(button_row)

        # Connect signals to event methods

        self.calc_button.clicked.connect(self.on_calc_button_clicked)
        self.expression_edit.returnPressed.connect(self.on_calc_button_clicked)
        self.close_button.clicked.connect(self.close)

    def on_calc_button_clicked(self):
        """Evaluate the expression and show the result or the error"""

        expression = self.expression_edit.text()

        try:
            result = eval(expression, {"__builtins__": {}}, MATH_NAMES)
        except Exception as e:
            self.result_edit.setText(f"Error: {e}")
            return

        self.result_edit.setText(str(result))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ExprEvalWindow()
    window.show()

    sys.exit(app.exec())
