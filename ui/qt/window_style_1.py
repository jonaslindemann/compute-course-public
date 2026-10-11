"""
Window flags control how the window system decorates a window.
Try the different flag combinations below.
"""

import sys

from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Qt


class MyWindow(QMainWindow):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__(None, Qt.WindowType.Window)
        # super().__init__(None, Qt.WindowType.Window | Qt.WindowType.Dialog)
        # super().__init__(None, Qt.WindowType.Window | Qt.WindowType.Tool)

        self.resize(300, 200)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
