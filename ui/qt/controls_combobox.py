# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

class MyWindow(QWidget):
    """Main class for our window"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.init_gui()

    def init_gui(self):

        # Configure window

        self.resize(400, 200)
        self.move(50, 50)
        self.setWindowTitle("ComboBox Example")

        # Create combobox control

        self.combo_box = QComboBox(self)
        self.combo_box.move(20, 20)

        # Add options

        self.combo_box.addItem("Alternative 1")
        self.combo_box.addItem("Alternative 2")
        self.combo_box.addItem("Alternative 3")
        self.combo_box.addItem("Alternative 4")

        # Set default selection

        self.combo_box.setCurrentIndex(3)

        # Connect event method to signal

        self.combo_box.currentIndexChanged.connect(self.on_current_index_changed)

    def on_current_index_changed(self, index):
        """Handle currentIndexChanged signal"""

        QMessageBox.information(self, "Message", "You selected: " + str(index))
        QMessageBox.information(self, "Message", "The text was: " + self.combo_box.currentText())
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())