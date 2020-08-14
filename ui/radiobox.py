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
        
        self.radioButton1 = QRadioButton("Extra allt", self.ui)
        self.radioButton1.move(20,20)
        self.radioButton2 = QRadioButton("More...", self.ui)
        self.radioButton2.move(20,50)
        self.radioButton1.clicked.connect(self.onRadioButtonClicked)
        self.radioButton2.clicked.connect(self.onRadioButtonClicked)
        
        self.radioButton1.setChecked(True)
        
    def onRadioButtonClicked(self):
        """Respond to button click"""
        if self.radioButton1.isChecked():
            QMessageBox.information(self.ui, "Meddelande", "Radio 1 checked")
        else:
            QMessageBox.information(self.ui, "Meddelande", "Radio 2 checked")
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
