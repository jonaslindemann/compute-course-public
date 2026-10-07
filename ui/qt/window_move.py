"""
Composition instead of inheritance: a class that owns a QMainWindow
instead of deriving from it.
"""

import sys

from qtpy.QtWidgets import QApplication, QMainWindow


class MyWindow:
    """Application class that owns a main window"""

    def __init__(self):
        """Class constructor"""

        self.ui = QMainWindow()
        self.ui.resize(640, 480)
        self.ui.move(50, 50)
        self.ui.setWindowTitle("MyWindow")

    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
