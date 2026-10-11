"""
Opening a window maximised or in full screen mode.
"""

import sys

from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Qt


class MyWindow(QMainWindow):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(200, 100)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")

        self.setWindowState(Qt.WindowState.WindowMaximized)
        # self.setWindowState(Qt.WindowState.WindowFullScreen)  # Close with Alt+F4


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
