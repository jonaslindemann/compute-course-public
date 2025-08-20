#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:10:06 2017

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy import uic
from random import *

class MainWindow(QMainWindow):
    """Main window class for the Flow application"""

    def __init__(self):
        """Class constructor"""
        
        super().__init__()

        # Load and show our user interface
        
        uic.loadUi("graphics_view_1.ui", self)
        
        self.scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setInteractive(True)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)  
                
        for i in range(100):
            line = self.scene.addLine(
                    uniform(-1000.0, 1000.0),
                    uniform(-1000.0, 1000.0),
                    uniform(-1000.0, 1000.0),
                    uniform(-1000.0, 1000.0),
                    QPen(Qt.red)
                    )

        self.graphics_view.show()

        self.resize(800, 800)

    def showEvent(self, event):
        self.graphics_view.fitInView(self.scene.sceneRect())
        self.graphics_view.centerOn(0,0)

    def resizeEvent(self, event):
        self.graphics_view.fitInView(self.scene.sceneRect())
        self.graphics_view.centerOn(0,0)

if __name__ == '__main__':    

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
