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
        self.ui.resize(400,200)
        self.ui.move(50,50)
        self.ui.setWindowTitle("MyWindow")
        
        self.listBox = QListWidget(self.ui)
        self.listBox.move(20,20)
        self.listBox.resize(100,100)
        self.listBox.addItem("Alt 1")
        self.listBox.addItem("Alt 2")
        self.listBox.addItem("Alt 3")
        self.listBox.addItem("Alt 4")
        self.listBox.currentRowChanged.connect(self.onCurrentRowChanged)
        
    def onCurrentRowChanged(self, curr):
        """Respond to button click"""
        QMessageBox.information(self.ui, "Meddelande", "Du valde: " + str(curr))

    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
