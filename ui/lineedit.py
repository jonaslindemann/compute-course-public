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
        
        self.button = QPushButton("Tryck", self.ui)
        self.button.move(50,50)
        self.button.resize(100,50)
        self.button.clicked.connect(self.onButtonClicked)

        
        self.lineEdit = QLineEdit(self.ui)
        self.lineEdit.move(20,20)
        self.lineEdit.setText("Text")
        
    def onButtonClicked(self):
        QMessageBox.information(self.ui, "Text", self.lineEdit.text())
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
