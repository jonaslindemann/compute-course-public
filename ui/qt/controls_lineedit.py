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

        # Configure window
        
        self.resize(400,200)
        self.move(50,50)
        self.setWindowTitle("MyWindow")

        # Create button
        
        self.button = QPushButton("Press", self)
        self.button.move(50,50)
        self.button.resize(100,50)
        self.button.clicked.connect(self.on_button_clicked)

        # Create text control

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(20,20)
        self.lineEdit.setText("Text")
        
    def on_button_clicked(self):
        """Event method for the clicked signal"""
        QMessageBox.information(self, "Text", self.lineEdit.text())
        

if __name__ == '__main__':
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
