"""
A main window class derived from QMainWindow.
"""

import sys

from qtpy.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(640, 480)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
