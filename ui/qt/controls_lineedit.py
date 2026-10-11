"""
QLineEdit example. Values are set with setText() and read with text().
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Configure window

        self.resize(300, 100)
        self.move(50, 50)
        self.setWindowTitle("LineEdit Example")

        # Create controls

        self.line_edit = QLineEdit()
        self.line_edit.setText("Text")

        self.button = QPushButton("Press")
        self.button.clicked.connect(self.on_button_clicked)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        layout.addStretch()

    def on_button_clicked(self):
        """Event method for the clicked signal"""
        QMessageBox.information(self, "Text", self.line_edit.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
