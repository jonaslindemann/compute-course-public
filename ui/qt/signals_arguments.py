"""
Passing extra arguments to slots: lambda and functools.partial.

Buttons created in a loop should all call the same method, but with
different values. The first row shows a common mistake: the lambda looks
up i when the button is clicked, not when it is created, so every button
reports the last value of the loop.

Note that clicked emits a bool (checked). A lambda with a default argument
must therefore accept that bool first, or it will overwrite our value.
"""

import sys
from functools import partial

from qtpy.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout,
)


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.move(50, 50)
        self.setWindowTitle("Slot arguments")

        self.result_label = QLabel("Click a button")

        grid = QGridLayout()

        # 1. Late binding (wrong). All buttons will report i = 4.

        grid.addWidget(QLabel("lambda (wrong)"), 0, 0)
        for i in range(5):
            button = QPushButton(str(i))
            button.clicked.connect(lambda: self.on_number_clicked(i, "lambda (wrong)"))
            grid.addWidget(button, 0, i + 1)

        # 2. Default argument binds the current value of i. The first
        #    parameter receives the checked argument from clicked.

        grid.addWidget(QLabel("lambda with default"), 1, 0)
        for i in range(5):
            button = QPushButton(str(i))
            button.clicked.connect(
                lambda checked=False, i=i: self.on_number_clicked(i, "lambda with default")
            )
            grid.addWidget(button, 1, i + 1)

        # 3. functools.partial binds the value when the connection is made.

        grid.addWidget(QLabel("functools.partial"), 2, 0)
        for i in range(5):
            button = QPushButton(str(i))
            button.clicked.connect(partial(self.on_number_clicked, i, "functools.partial"))
            grid.addWidget(button, 2, i + 1)

        # Layout

        layout = QVBoxLayout(self)
        layout.addLayout(grid)
        layout.addWidget(self.result_label)

    def on_number_clicked(self, value, method, checked=False):
        """Slot shared by all buttons"""
        self.result_label.setText(f"{method}: value = {value}")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
