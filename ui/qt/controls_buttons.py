# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton
from qtpy.QtCore import *

class MyWindow(QWidget):
    def __init__(self):
        """MyWindow constructor"""
        super().__init__()

        # Create interface controls

        self.init_gui()

    def init_gui(self):
        """Initialize interface"""

        # Create a button control

        self.button1 = QPushButton("Press me", self)
        self.button1.resize(100,30)
        self.button1.move(20,20)

        self.button2 = QPushButton("Press me", self)
        self.button2.resize(100,30)
        self.button2.move(20+120,20)

        self.button3 = QPushButton("Press me", self)
        self.button3.resize(100,30)
        self.button3.move(20+120*2,20)

        # Connect method to the clicked signal

        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)

        # Set window properties

        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle("Button Example")

        # Show window

        self.show()

    def on_button1_clicked(self):
        """Event method for the clicked signal"""
        if self.button2.isVisible():
            self.button2.setVisible(False)
        else:
            self.button2.setVisible(True)

    def on_button2_clicked(self):
        """Event method for the clicked signal"""
        if self.button3.isEnabled():
            self.button3.setEnabled(False)
        else:
            self.button3.setEnabled(True)

if __name__ == "__main__":  

    app = QApplication(sys.argv)

    # Create our MyWindow object

    window = MyWindow()

    # Start event loop

    sys.exit(app.exec_())
