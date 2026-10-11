"""
Sorting an item based QTableWidget. A custom QTableWidgetItem compares
numbers numerically instead of as text.
"""

import sys
from numbers import Number
from pathlib import Path

import pandas as pd

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from qtpy.QtCore import Qt

HERE = Path(__file__).resolve().parent


class NumericTableWidgetItem(QTableWidgetItem):
    """Table item that sorts numeric values numerically"""

    def __init__(self, value):
        """Class constructor"""
        super().__init__(str(value))
        self.value = value

    def __lt__(self, other):
        """Less than operator used by the table when sorting"""
        if isinstance(self.value, Number) and isinstance(other.value, Number):
            return self.value < other.value
        return super().__lt__(other)


class ItemTableWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Load CSV data

        self.df = pd.read_csv(HERE / "Cost_of_Living_Index_by_Country_2024.csv")

        # Create table

        self.item_table = QTableWidget()
        self.item_table.verticalHeader().setVisible(False)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.item_table)

        # Set window title and size

        self.setWindowTitle("Sorted item based table")
        self.resize(800, 800)

        # Fill table, then enable sorting. Sorting must be disabled while
        # filling, otherwise rows move around as items are inserted.

        self.update_controls()
        self.item_table.setSortingEnabled(True)
        self.item_table.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def update_controls(self):
        """Fill the table from the DataFrame"""

        self.item_table.setSortingEnabled(False)
        self.item_table.clear()
        self.item_table.setRowCount(len(self.df.index))
        self.item_table.setColumnCount(len(self.df.columns))
        self.item_table.setHorizontalHeaderLabels([str(c) for c in self.df.columns])

        for row in range(len(self.df.index)):
            for col in range(len(self.df.columns)):
                value = self.df.iloc[row, col]
                self.item_table.setItem(row, col, NumericTableWidgetItem(value))

        self.item_table.resizeColumnsToContents()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ItemTableWindow()
    window.show()

    sys.exit(app.exec())
