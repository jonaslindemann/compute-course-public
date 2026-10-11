"""
Model/view: a QTableView showing a pandas DataFrame through a
QAbstractTableModel. The view only asks for the cells it displays,
so this scales to large data sets.
"""

import sys
from pathlib import Path

import pandas as pd

from qtpy.QtWidgets import QApplication, QMainWindow, QTableView
from qtpy.QtCore import Qt, QAbstractTableModel, QModelIndex

HERE = Path(__file__).resolve().parent


class PandasModel(QAbstractTableModel):
    """Read-only table model for a pandas DataFrame"""

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            return str(self._data.index[section])
        return None


class MainWindow(QMainWindow):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.setWindowTitle("CSV Viewer")
        self.resize(800, 800)

        # Read CSV file and create the model

        self.df = pd.read_csv(HERE / "Cost_of_Living_Index_by_Country_2024.csv")
        self.model = PandasModel(self.df)

        # Create the table view and connect it to the model

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()

        # Sorting requires the model to implement sort(), see
        # table_view_model_sorted.py

        self.setCentralWidget(self.table)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
