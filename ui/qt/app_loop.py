# -*- coding: utf-8 -*-

import sys, os

from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtCore import Qt

if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = QWidget()
    widget.show()

    sys.exit(app.exec_())
