"""
A menu connected to a QAction.
"""

import sys

from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox
from qtpy.QtGui import QAction


class MyWindow(QMainWindow):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 200)
        self.move(50, 50)
        self.setWindowTitle("Menu Example")

        # Define action

        self.my_action = QAction("MyAction", self)
        self.my_action.setShortcut("Ctrl+T")
        self.my_action.triggered.connect(self.on_my_action)

        # Connect action to menu

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.my_action)

    def on_my_action(self):
        """Method for handling MyAction"""
        QMessageBox.information(self, "Message", "Ouch!")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
