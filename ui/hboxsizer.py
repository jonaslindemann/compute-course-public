# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from PyQt5.QtWidgets import *

class MyWindow:
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        
        self.ui = QMainWindow()
        self.ui.resize(200,200)
        self.ui.move(50,50)
        self.ui.setWindowTitle("MyWindow")
        
        self.mainWidget = QWidget(self.ui)
        
        self.button1 = QPushButton("Button1")
        self.button2 = QPushButton("Button2")
        self.button3 = QPushButton("Button3")
        self.button4 = QPushButton("Button4")
        
        self.hbox = QHBoxLayout(self.ui)
        self.hbox.addWidget(self.button1)
        self.hbox.addWidget(self.button2)
        self.hbox.addWidget(self.button3)
        self.hbox.addWidget(self.button4)
        
        self.mainWidget.setLayout(self.hbox)
        self.ui.setCentralWidget(self.mainWidget)
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
