# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *

class MyWindow(QWidget):
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(400,200)
        self.move(50,50)
        self.setWindowTitle("MyWindow")
        
        self.button = QPushButton("Tryck", self)
        self.button.move(50,50)
        self.button.resize(100,50)
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        """Respond to button click"""
        QMessageBox.information(self, "Meddelande", "Ouch!")
            

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
