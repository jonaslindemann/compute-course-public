import sys
import pandas as pd
from qtpy.QtWidgets import QApplication, QTableView, QMainWindow
from qtpy.QtCore import Qt, QAbstractTableModel, QModelIndex

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.resize(800, 800)

        # Read CSV file
        print("Reading CSV file...")
        self.df = pd.read_csv('Cost_of_Living_Index_by_Country_2024.csv')  # Replace with your CSV file path
        print("CSV file read")

        # Create and set the model
        print("Creating model...")
        model = PandasModel(self.df)

        # Create the table view
        print("Creating table view...")
        self.table = QTableView()
        self.table.setModel(model)
        self.table.verticalHeader().setVisible(False)

        print("Setting up table view...")
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


        # Enable sorting
        self.table.setSortingEnabled(True)

        # Set the table as the central widget
        self.setCentralWidget(self.table)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())