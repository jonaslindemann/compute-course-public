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

        self.init_gui()

    def init_gui(self):

        self.resize(200,200)
        self.move(50,50)
        self.setWindowTitle("MyWindow")
        
        self.button1 = QPushButton('Button1')
        self.button2 = QPushButton('Button2')
        self.button3 = QPushButton('Button3')
        self.button4 = QPushButton('Button4')
        
        self.button5 = QPushButton('Button5')
        self.button6 = QPushButton('Button6')
        self.button7 = QPushButton('Button7')
        self.button8 = QPushButton('Button8')

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)
        
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.button5)
        self.hbox.addWidget(self.button6)
        self.hbox.addWidget(self.button7)
        self.hbox.addWidget(self.button8)

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)


if __name__ == '__main__':
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
