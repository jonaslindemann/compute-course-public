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
        
        self.comboBox = QComboBox(self.ui)
        self.comboBox.move(20,20)
        self.comboBox.addItem("Alt 1")
        self.comboBox.addItem("Alt 2")
        self.comboBox.addItem("Alt 3")
        self.comboBox.addItem("Alt 4")
        self.comboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        
    def onCurrentIndexChanged(self, index):
        """Respond to button click"""
        QMessageBox.information(self.ui, "Meddelande", "Du valde: " + str(index))
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())