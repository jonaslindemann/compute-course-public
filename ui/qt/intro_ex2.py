"""
Deriving our own window class from QWidget.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """MyWindow constructor"""
        print("Initializing MyWindow")
        super().__init__()

        # Set window properties

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("MyWindow")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Create and show our MyWindow object

    window = MyWindow()
    window.show()

    # Enter event loop

    sys.exit(app.exec())
