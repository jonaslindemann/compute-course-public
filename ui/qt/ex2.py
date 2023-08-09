# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtCore import *

class MyWindow(QWidget):
    def __init__(self):
        """MyWindow constructor"""

        super().__init__()

        # Skapa gränssnittskontroller

        self.init_gui()

    def init_gui(self):
        """Initiera gränssnitt"""

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("MyWindow")

        # Visa fönster

        self.show()

if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)

    # Skapa vårt MyWindow objekt

    window = MyWindow()

    # Starta händelseloop

    sys.exit(app.exec_())
