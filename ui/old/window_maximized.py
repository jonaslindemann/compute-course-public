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
        self.ui.resize(200,100)
        self.ui.move(50,50)
        self.ui.setWindowTitle("MyWindow")
        
    def show(self):
        """Show and raise window"""
        self.ui.setWindowState(Qt.WindowMaximized)
        #self.ui.setWindowState(QtCore.Qt.WindowFullScreen)
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
