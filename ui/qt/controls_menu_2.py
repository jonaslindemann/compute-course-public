# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

class MyWindow(QMainWindow):
    """Main class for our window"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(400, 200)
        self.move(50, 50)
        self.setWindowTitle("Menu Example")

        # Define actions

        self.new_file_action = QAction("New", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.new_file_action.triggered.connect(self.on_new_file_action)

        self.open_file_action = QAction("Open...", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.triggered.connect(self.on_open_file_action)

        self.save_file_action = QAction("Save", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.triggered.connect(self.on_save_file_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Alt+F4")
        self.exit_action.triggered.connect(self.on_exit)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.on_cut_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.on_copy_action)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.on_paste_action)

        # Connect menus to actions

        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = self.menuBar().addMenu("Edit")
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

        # Show window

        self.show()

    def on_new_file_action(self):
        """Event method for menu event"""
        print("New file!")

    def on_open_file_action(self):
        """Event method for menu event"""
        print("Open file")

    def on_save_file_action(self):
        """Event method for menu event"""
        print("Save file")

    def on_exit(self):
        """Event method for menu event"""
        self.close()

    def on_cut_action(self):
        """Event method for menu event"""
        print("Cut")

    def on_copy_action(self):
        """Event method for menu event"""
        print("Copy")

    def on_paste_action(self):
        """Event method for menu event"""
        print("Paste")


if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
