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

        uic.loadUi("controls_form_ui.ui", self)

        self.push_button_1.setText("Press me!")


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
