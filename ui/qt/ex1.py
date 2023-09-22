# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtCore import *

if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)

    widget = QWidget()
    widget.resize(250, 150)
    widget.move(300, 300)
    widget.setWindowTitle('Hello Qt')
    widget.show()

    print("Before application loop.")
    app.exec_()
    print("Last window closed.")
