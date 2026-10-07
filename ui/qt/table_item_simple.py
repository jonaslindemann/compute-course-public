"""
Showing a pandas DataFrame in an item based QTableWidget.

Every cell becomes a QTableWidgetItem. Simple, but slow for large data.
See table_view_model.py for the model/view alternative.
"""

import sys
from pathlib import Path

import pandas as pd

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

HERE = Path(__file__).resolve().parent


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

        self.setWindowTitle("Item based table")
        self.resize(800, 800)

        # Fill table. Done before connecting signals, so that filling the
        # table does not trigger itemChanged for every cell.

        self.update_controls()

        # Connect signals

        self.item_table.itemChanged.connect(self.on_item_changed)
        self.item_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.item_table.cellClicked.connect(self.on_cell_clicked)

    def update_controls(self):
        """Fill the table from the DataFrame"""

        self.item_table.clear()
        self.item_table.setRowCount(len(self.df.index))
        self.item_table.setColumnCount(len(self.df.columns))
        self.item_table.setHorizontalHeaderLabels([str(c) for c in self.df.columns])

        for row in range(len(self.df.index)):
            for col in range(len(self.df.columns)):
                value = self.df.iloc[row, col]
                self.item_table.setItem(row, col, QTableWidgetItem(str(value)))

        self.item_table.resizeColumnsToContents()

    def on_item_changed(self, item):
        """Called when a cell has been edited"""
        print("Item changed:", item.row(), item.column(), item.text())

    def on_selection_changed(self):
        """Called when the selection changes"""
        print("Selection changed:", [item.text() for item in self.item_table.selectedItems()])

    def on_cell_clicked(self, row, col):
        """Called when a cell is clicked"""
        print("Cell clicked:", row, col)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ItemTableWindow()
    window.show()

    sys.exit(app.exec())
