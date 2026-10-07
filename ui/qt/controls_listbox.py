"""
QListWidget example. Scrollbars are added automatically when needed.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Set window properties

        self.resize(300, 400)
        self.move(50, 50)
        self.setWindowTitle("ListWidget Example")

        # Create list control and add options

        self.list_widget = QListWidget()
        self.list_widget.addItems([f"Option {i}" for i in range(100)])

        # Set the default option to row 2

        self.list_widget.setCurrentRow(2)

        # Connect an event method to the signal

        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)

    def on_current_row_changed(self, row):
        """Handle the currentRowChanged signal"""
        QMessageBox.information(
            self, "Message", f"You selected row {row}: {self.list_widget.currentItem().text()}"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
