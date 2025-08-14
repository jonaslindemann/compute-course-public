# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

class MyWindow(QWidget):
    """Main class for the window"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Configure window

        self.resize(400, 200)
        self.move(50, 50)
        self.setWindowTitle("MyWindow")

        # Create button

        self.button = QPushButton("Press", self)
        self.button.move(230, 18)
        self.button.clicked.connect(self.on_button_clicked)

        # Create text label

        self.label = QLabel("Text box", self)
        self.label.move(20, 22)

        # Create text control

        self.line_edit = QLineEdit(self)
        self.line_edit.move(80, 20)
        self.line_edit.setText("Text")

        # Create label control with image.

        self.image_label = QLabel("Image", self)
        self.image_label.move(20, 60)
        self.image_label.setScaledContents(True)
        self.image_label.resize(300, 100)
        self.image_label.setPixmap(QPixmap("python_logo.png"))

        self.show()

    def on_button_clicked(self):
        """Event method for the clicked signal"""
        QMessageBox.information(self, "Text", self.line_edit.text())


if __name__ == "__main__":     

    app = QApplication(sys.argv)

    # Create our MyWindow object

    window = MyWindow()

    # Start event loop

    sys.exit(app.exec_())
