# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *

class MyWindow(QWidget):
    """Main class for the window"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Set window properties

        self.resize(700,400)
        self.move(50,50)
        self.setWindowTitle("Table example")

        # Create buttons to interact with the table

        self.add_row_button = QPushButton("Add row", self)
        self.add_row_button.move(580, 20)
        self.add_col_button = QPushButton("Add column", self)
        self.add_col_button.move(580, 50)
        self.show_selected_button = QPushButton("Show content", self)
        self.show_selected_button.move(580, 80)
        self.clear_button = QPushButton("Clear table", self)
        self.clear_button.move(580, 110)

        # Create table widget

        self.table = QTableWidget(5, 10, self)
        self.table.move(20,20)
        self.table.resize(550,350)

        # Fill table with data

        self.fill_table()

        # Set table headers

        self.update_headers()

        # Connect signals to events

        self.add_row_button.clicked.connect(self.on_add_row_button_clicked)
        self.add_col_button.clicked.connect(self.on_add_col_button_clicked)
        self.show_selected_button.clicked.connect(self.on_show_selected_button_clicked)
        self.clear_button.clicked.connect(self.on_clear_button_clicked)

        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.currentCellChanged.connect(self.on_current_cell_changed)


    def fill_table(self):
        """Fill the table with values"""
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.setItem(r, c, QTableWidgetItem("%d,%d" % (r, c)))

    def update_headers(self):
        """Update table headers"""
        for r in range(self.table.rowCount()):
            self.table.setVerticalHeaderItem(r, QTableWidgetItem("Row%d" % r))

        for c in range(self.table.columnCount()):
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem("Col%d" % c))

    def on_add_row_button_clicked(self):
        """Add row"""
        self.table.setRowCount(self.table.rowCount()+1)
        self.update_headers()

    def on_add_col_button_clicked(self):
        """Add column"""
        self.table.setColumnCount(self.table.columnCount()+1)
        self.update_headers()

    def on_show_selected_button_clicked(self):
        """Show content of selected cell"""
        if self.table.currentItem()!=None:
            QMessageBox.information(self, "Text", self.table.currentItem().text())

    def on_clear_button_clicked(self):
        """Clear table content"""
        self.table.clear()
        self.update_headers()

    def on_cell_clicked(self, row, col):
        print("on_cell_clicked %d, %d" % (row, col))

    def on_current_cell_changed(self, current_row, current_col, prev_row, prev_col):
        print("on_current_cell_changed %d, %d previous %d, %d" % (current_row, current_col, prev_row, prev_col))





if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
