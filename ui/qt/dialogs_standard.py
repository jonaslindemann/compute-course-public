# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

class MyWindow(QMainWindow):
    """Main Window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(500, 100)
        self.move(50, 50)
        self.setWindowTitle("Message Boxes Example")

        self.button1 = QPushButton("Information", self)
        self.button1.resize(100,30)
        self.button1.move(20,20)

        self.button2 = QPushButton("Warning", self)
        self.button2.resize(100,30)
        self.button2.move(20+120,20)

        self.button3 = QPushButton("Critical", self)
        self.button3.resize(100,30)
        self.button3.move(20+120*2,20)

        self.button4 = QPushButton("Question", self)
        self.button4.resize(100,30)
        self.button4.move(20+120*3,20)

        self.button5 = QPushButton("Open File", self)
        self.button5.resize(100,30)
        self.button5.move(20,60)

        self.button6 = QPushButton("Save file", self)
        self.button6.resize(100,30)
        self.button6.move(20+120,60)


        # Connect method to the clicked signal

        self.button1.clicked.connect(self.on_info_dialog)
        self.button2.clicked.connect(self.on_warning_dialog)
        self.button3.clicked.connect(self.on_critical_dialog)
        self.button4.clicked.connect(self.on_question_dialog)
        self.button5.clicked.connect(self.on_open_file_dialog)
        self.button6.clicked.connect(self.on_save_file_dialog)


    def on_info_dialog(self):
        """Method for handling MyAction"""
        QMessageBox.information(self, "Meddelande", "Detta är ett informativt meddelande.")

    def on_warning_dialog(self):
        """Method for handling MyAction"""
        QMessageBox.warning(self, "Meddelande", "Detta är ett varningsmeddelande.")

    def on_critical_dialog(self):
        """Method for handling MyAction"""
        QMessageBox.critical(self, "Meddelande", "Detta är ett kritiskt meddelande.")

    def on_question_dialog(self):
        """Method for handling MyAction"""
        reply = QMessageBox.question(self, "Meddelande", "Är du säker?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Val", "Användaren valde Ja")
        else:
            QMessageBox.information(self, "Val", "Användaren valde Nej")

    def on_open_file_dialog(self):
        """Method for handling MyAction"""
        filename, _ = QFileDialog.getOpenFileName(self, "Öppna fil", "", "All Files (*)")
        if filename:
            QMessageBox.information(self, "Val", f"Vald fil: {filename}")
        else:
            QMessageBox.information(self, "Val", "Ingen fil vald")

    def on_save_file_dialog(self):
        """Method for handling MyAction"""
        filename, _ = QFileDialog.getSaveFileName(self, "Spara fil", "", "All Files (*)")
        if filename:
            QMessageBox.information(self, "Val", f"Fil sparad som: {filename}")
        else:
            QMessageBox.information(self, "Val", "Ingen fil sparad")
        

if __name__ == '__main__':
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())
    