#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:10:06 2017

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy import uic
from random import *

import pandas as pd


class ItemTableWindow(QWidget):
    """Main window class for the Flow application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Load CSV data

        self.df = pd.read_csv("Cost_of_Living_Index_by_Country_2024.csv")

        # Load and show our user interface

        self.item_table = QTableWidget(5, 3, self)
        self.item_table.verticalHeader().setVisible(False)
        self.item_table.setSortingEnabled(False)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.item_table)

        self.update_controls()
        self.enable_sorting()

        self.item_table.show()

        self.resize(800, 800)

    def update_controls(self):
        # Set table dimensions
        self.item_table.setColumnCount(len(self.df.columns))
        self.item_table.setRowCount(len(self.df.index))

        # Set headers
        self.item_table.setHorizontalHeaderLabels(self.df.columns)

        # Populate table
        for row in range(len(self.df.index)):
            for col in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[row, col]))
                self.item_table.setItem(row, col, item)

        self.item_table.resizeColumnsToContents()
        self.item_table.resizeRowsToContents()

    def enable_sorting(self):
        self.item_table.setSortingEnabled(False)





if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = ItemTableWindow()
    window.show()

    sys.exit(app.exec_())
