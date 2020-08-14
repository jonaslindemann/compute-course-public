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
        
        # Define action
        
        self.actionDialog = QAction("Open dialog", self.ui)
        self.actionDialog.setShortcut("Ctrl-T")
        self.actionDialog.triggered.connect(self.onDialog)
        
        # Connect action to menu

        self.fileMenu = self.ui.menuBar().addMenu("File")
        self.fileMenu.addAction(self.actionDialog)
                
    def onDialog(self):
        """Method for handling MyAction"""
        result = QMessageBox.question(
            self.ui, "Meddelande", "Ta bort?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            QMessageBox.information(self.ui, "Val", "Du valde Yes")
        else:
            QMessageBox.information(self.ui, "Val", "Du valde No")
            
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
