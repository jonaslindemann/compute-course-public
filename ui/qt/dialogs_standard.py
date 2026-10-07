"""
Standard dialogs: message boxes and file dialogs.
"""

import sys

from qtpy.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QFileDialog,
)


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.move(50, 50)
        self.setWindowTitle("Standard Dialogs Example")

        # Create buttons

        self.info_button = QPushButton("Information")
        self.warning_button = QPushButton("Warning")
        self.critical_button = QPushButton("Critical")
        self.question_button = QPushButton("Question")
        self.open_button = QPushButton("Open file")
        self.save_button = QPushButton("Save file")

        # Layout

        grid = QGridLayout(self)
        grid.addWidget(self.info_button, 0, 0)
        grid.addWidget(self.warning_button, 0, 1)
        grid.addWidget(self.critical_button, 0, 2)
        grid.addWidget(self.question_button, 0, 3)
        grid.addWidget(self.open_button, 1, 0)
        grid.addWidget(self.save_button, 1, 1)

        # Connect methods to the clicked signal

        self.info_button.clicked.connect(self.on_info_dialog)
        self.warning_button.clicked.connect(self.on_warning_dialog)
        self.critical_button.clicked.connect(self.on_critical_dialog)
        self.question_button.clicked.connect(self.on_question_dialog)
        self.open_button.clicked.connect(self.on_open_file_dialog)
        self.save_button.clicked.connect(self.on_save_file_dialog)

    def on_info_dialog(self):
        """Show an information message"""
        QMessageBox.information(self, "Message", "This is an informative message.")

    def on_warning_dialog(self):
        """Show a warning message"""
        QMessageBox.warning(self, "Message", "This is a warning message.")

    def on_critical_dialog(self):
        """Show a critical message"""
        QMessageBox.critical(self, "Message", "This is a critical message.")

    def on_question_dialog(self):
        """Ask a yes/no question"""
        reply = QMessageBox.question(
            self, "Message", "Are you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Choice", "You selected Yes")
        else:
            QMessageBox.information(self, "Choice", "You selected No")

    def on_open_file_dialog(self):
        """Select a file to open"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Python files (*.py);;All files (*)"
        )
        if filename:
            QMessageBox.information(self, "Choice", f"Selected file: {filename}")
        else:
            QMessageBox.information(self, "Choice", "No file selected")

    def on_save_file_dialog(self):
        """Select a file name to save to"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text files (*.txt);;All files (*)"
        )
        if filename:
            QMessageBox.information(self, "Choice", f"Save as: {filename}")
        else:
            QMessageBox.information(self, "Choice", "No file selected")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
