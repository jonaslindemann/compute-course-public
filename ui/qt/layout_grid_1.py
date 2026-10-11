"""
QGridLayout with size policies, margins, spacing and stretch factors.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSizePolicy


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(400, 400)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")

        self.grid = QGridLayout(self)

        # Create a 3 x 3 grid of buttons that expand to fill their cells

        self.buttons = []

        for row in range(3):
            for col in range(3):
                button = QPushButton(f"Button{row * 3 + col + 1}")
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.grid.addWidget(button, row, col)
                self.buttons.append(button)

        # Margins and spacing

        self.grid.setContentsMargins(20, 40, 20, 40)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(20)

        # The middle row and column get 4 times the space of the others

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 4)
        self.grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 4)
        self.grid.setRowStretch(2, 1)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
