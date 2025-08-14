#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:10:06 2017

@author: lindemann
"""

import sys

from qtpy.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QApplication
from qtpy.QtCore import Qt

import numpy as np
import pandas as pd


class ItemTableWindow(QWidget):
    """Main window class for the Flow application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Load CSV data

        self.df = pd.read_csv("Cost_of_Living_Index_by_Country_2024.csv")

        # Create table

        self.item_table = QTableWidget(5, 3, self)
        self.item_table.verticalHeader().setVisible(False)

        # Set layout

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.item_table)

        # Set window title and size

        self.setWindowTitle("Item based table")
        self.resize(800, 800)

        # Update controls

        self.update_controls()

        # Show table

        self.item_table.show()

        # Connect signals

        self.item_table.itemChanged.connect(self.on_item_changed)
        self.item_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.item_table.cellClicked.connect(self.on_cell_clicked)



    def update_controls(self):
        """Update table control"""

        # Clear table

        self.item_table.clear()

        # Set number of rows and columns

        self.item_table.setColumnCount(len(self.df.columns))
        self.item_table.setRowCount(len(self.df.index))
        

        # Set headers

        self.item_table.setHorizontalHeaderLabels(self.df.columns)

        # Populate table

        for row in range(len(self.df.index)):
            for col, _ in enumerate(self.df.columns):
                value = self.df.iloc[row, col]
                item = QTableWidgetItem(str(value))
                #item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.item_table.setItem(row, col, item)

        # Resize table

        self.item_table.resizeColumnsToContents()
        self.item_table.resizeRowsToContents()

    def on_item_changed(self, item):
        print("Item changed: ", item.row(), item.column(), item.text())

    def on_selection_changed(self):
        print("Selection changed: ", self.item_table.selectedItems())

    def on_cell_clicked(self, row, col):
        print("Cell clicked: ", row, col)


if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = ItemTableWindow()
    window.show()

    sys.exit(app.exec_())
