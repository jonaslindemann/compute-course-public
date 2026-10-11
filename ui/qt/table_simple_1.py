"""
QTableWidget basics: adding rows and columns, headers, and cell signals.
"""

import sys

from qtpy.QtWidgets import (
    QApplication, QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QVBoxLayout, QMessageBox,
)


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Set window properties

        self.resize(700, 400)
        self.move(50, 50)
        self.setWindowTitle("Table example")

        # Create table widget and buttons

        self.table = QTableWidget(5, 10)

        self.add_row_button = QPushButton("Add row")
        self.add_col_button = QPushButton("Add column")
        self.show_selected_button = QPushButton("Show content")
        self.clear_button = QPushButton("Clear table")

        # Layout: table to the left, buttons stacked to the right

        buttons = QVBoxLayout()
        buttons.addWidget(self.add_row_button)
        buttons.addWidget(self.add_col_button)
        buttons.addWidget(self.show_selected_button)
        buttons.addWidget(self.clear_button)
        buttons.addStretch()

        layout = QHBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(buttons)

        # Fill table with data and set headers

        self.fill_table()
        self.update_headers()

        # Connect signals to event methods

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
                self.table.setItem(r, c, QTableWidgetItem(f"{r},{c}"))

    def update_headers(self):
        """Update table headers"""
        self.table.setVerticalHeaderLabels([f"Row{r}" for r in range(self.table.rowCount())])
        self.table.setHorizontalHeaderLabels([f"Col{c}" for c in range(self.table.columnCount())])

    def on_add_row_button_clicked(self):
        """Add a row"""
        self.table.setRowCount(self.table.rowCount() + 1)
        self.update_headers()

    def on_add_col_button_clicked(self):
        """Add a column"""
        self.table.setColumnCount(self.table.columnCount() + 1)
        self.update_headers()

    def on_show_selected_button_clicked(self):
        """Show content of the selected cell"""
        item = self.table.currentItem()
        if item is not None:
            QMessageBox.information(self, "Text", item.text())

    def on_clear_button_clicked(self):
        """Clear table content"""
        self.table.clear()
        self.update_headers()

    def on_cell_clicked(self, row, col):
        """Called when a cell is clicked"""
        print(f"on_cell_clicked {row}, {col}")

    def on_current_cell_changed(self, current_row, current_col, prev_row, prev_col):
        """Called when the current cell changes"""
        print(f"on_current_cell_changed {current_row}, {current_col} previous {prev_row}, {prev_col}")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
