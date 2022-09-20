# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

from qtpy import uic

class MainWindow(QWidget):
    """Main window class for the Flow application"""

    def __init__(self):
        """Class constructor"""

        super().__init__()

        # Load and show our user interface

        self.init_gui()

    def init_gui(self):
        """Initialisera gränssnitt"""

        uic.loadUi("form.ui", self)

        self.push_button_1.setText("Press me!")


if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons    

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
