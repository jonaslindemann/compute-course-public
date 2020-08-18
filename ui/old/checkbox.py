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
        
        self.checkBox = QCheckBox("Extra allt", self.ui)
        self.checkBox.move(20,20)
        self.checkBox.setChecked(True)
        self.checkBox.stateChanged.connect(self.onStateChange)
        
    def onStateChange(self):
        """Respond to button click"""
        if self.checkBox.checkState():
            QMessageBox.information(self.ui, "Meddelande", "Extra allt")
        else:
            QMessageBox.information(self.ui, "Meddelande", "Inget")
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())