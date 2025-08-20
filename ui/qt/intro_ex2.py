# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtCore import *

class MyWindow(QWidget):
    def __init__(self):
        """MyWindow constructor"""

        super().__init__()

        # Skapa gränssnittskontroller

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("MyWindow")

        # Visa fönster

        self.show()

if __name__ == "__main__": 

    app = QApplication(sys.argv)

    # Skapa vårt MyWindow objekt

    window = MyWindow()

    # Starta händelseloop

    sys.exit(app.exec_())
