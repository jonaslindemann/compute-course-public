"""
QHBoxLayout: controls placed side by side.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(200, 200)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")

        self.button1 = QPushButton("Button1")
        self.button2 = QPushButton("Button2")
        self.button3 = QPushButton("Button3")
        self.button4 = QPushButton("Button4")

        # Passing self to the layout constructor sets it as the window layout

        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.button1)
        self.hbox.addWidget(self.button2)
        self.hbox.addWidget(self.button3)
        self.hbox.addWidget(self.button4)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
