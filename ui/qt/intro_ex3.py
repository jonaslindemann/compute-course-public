"""
Adding a control to a window using absolute positioning.

Absolute positioning is only used here to introduce controls. See the
layout_*.py examples for the recommended way of placing controls.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """MyWindow constructor"""
        super().__init__()

        # Create a button control

        self.button = QPushButton("Press me", self)
        self.button.setToolTip("I am a button. Please press me")
        self.button.resize(100, 50)
        self.button.move(50, 50)

        # Connect method to the clicked signal

        self.button.clicked.connect(self.on_button_clicked)

        # Set window properties

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("MyWindow")

    def on_button_clicked(self):
        """Event method for the clicked signal"""
        print("Hello")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
