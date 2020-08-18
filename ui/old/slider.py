# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyWindow:
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        
        self.ui = QMainWindow()
        self.ui.resize(400,200)
        self.ui.move(50,50)
        self.ui.setWindowTitle("MyWindow")
        
        self.slider = QSlider(Qt.Vertical, self.ui)
        self.slider.move(20,20)
        self.slider.setMaximum(100)
        self.slider.setMinimum(0)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.onValueChanged)
        
    def onValueChanged(self, value):
        """Respond to button click"""
        print(value)
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
