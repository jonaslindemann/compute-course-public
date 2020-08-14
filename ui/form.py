# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

class MainWindow:
    """Main window class for the Flow application"""

    def __init__(self, app):
        """Class constructor"""

        # Assign our application instance as a member variable
        
        self.app = app
                
        # Load and show our user interface
        
        self.ui = uic.loadUi('form.ui')
        
        self.ui.show()
        self.ui.raise_()
        

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow(app)
    
    sys.exit(app.exec_())
