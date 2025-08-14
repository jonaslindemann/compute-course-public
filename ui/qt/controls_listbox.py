# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import QWidget, QListWidget, QMessageBox, QApplication
from qtpy.QtCore import *

class MyWindow(QWidget):
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Set window properties

        self.resize(450, 450)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")

        # Create list control

        self.list_box = QListWidget(self)
        self.list_box.move(20, 20)
        self.list_box.resize(400, 400)

        # Add options to the list

        for i in range(100):
            self.list_box.addItem("Option %d" % i)

        # Set the default option to row 2

        self.list_box.setCurrentRow(2)

        # Connect an event method to the signal

        self.list_box.currentRowChanged.connect(self.on_current_row_changed)

    def on_current_row_changed(self, curr):
        """Handle the currentRowChanged signal"""
        
        QMessageBox.information(self, "Message", "You selected: " + str(curr))
        QMessageBox.information(self, "Message", "The row contained: " + self.list_box.currentItem().text())


if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
