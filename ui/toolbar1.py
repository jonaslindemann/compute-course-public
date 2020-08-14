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
        
        self.actionMyAction = QAction("MyAction", self.ui)
        self.actionMyAction.setShortcut("Ctrl-T")
        self.actionMyAction.triggered.connect(self.onMyAction)
        
        # Connect action to menu

        self.fileMenu = self.ui.menuBar().addMenu("File")
        self.fileMenu.addAction(self.actionMyAction)
        
        # Create a toolbar
        
        self.toolbar = self.ui.addToolBar("MyToolbar")
        self.toolbar.addAction(self.actionMyAction)
        
    def onMyAction(self):
        """Method for handling MyAction"""
        QMessageBox.information(self.ui, "Meddelande", "Ouch!")
        
    def show(self):
        """Show and raise window"""
        self.ui.show()
        self.ui.raise_()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
