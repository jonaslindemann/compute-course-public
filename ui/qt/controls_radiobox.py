# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

class MyWindow(QWidget):
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()
        
        self.resize(400,100)
        self.move(50,50)
        self.setWindowTitle("Radio Button Example")
        
        self.radio_button1 = QRadioButton("Everything extra", self)
        self.radio_button1.move(20,20)
        self.radio_button2 = QRadioButton("More...", self)
        self.radio_button2.move(20,50)
        self.radio_button1.clicked.connect(self.on_radio_button_clicked)
        self.radio_button2.clicked.connect(self.on_radio_button_clicked)
        
        self.radio_button1.setChecked(True)
        
    def on_radio_button_clicked(self):
        """Respond to radio button selection"""
        if self.radio_button1.isChecked():
            QMessageBox.information(self, "Message", "Radio 1 selected")
        else:
            QMessageBox.information(self, "Message", "Radio 2 selected")
        
        
if __name__ == '__main__':    

    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
