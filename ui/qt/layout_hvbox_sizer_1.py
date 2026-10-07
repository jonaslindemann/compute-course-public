"""
Nesting layouts: a QHBoxLayout inside a QVBoxLayout, separated by a stretch.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout


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

        self.button5 = QPushButton("Button5")
        self.button6 = QPushButton("Button6")
        self.button7 = QPushButton("Button7")
        self.button8 = QPushButton("Button8")

        # Top level layout, set as the window layout

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)

        # Nested layout. No parent, as it is added to self.vbox below.

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button5)
        self.hbox.addWidget(self.button6)
        self.hbox.addWidget(self.button7)
        self.hbox.addWidget(self.button8)

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
