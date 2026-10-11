"""
Connecting a signal to a method that reads the value of another control.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMessageBox


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """MyWindow constructor"""
        super().__init__()

        # Create controls

        self.line_edit = QLineEdit(self)
        self.line_edit.move(50, 20)
        self.line_edit.setText("Text")

        self.button = QPushButton("Press me", self)
        self.button.setToolTip("I am a button. Please press me")
        self.button.resize(self.button.sizeHint())
        self.button.move(50, 50)

        # Connect method to the clicked signal

        self.button.clicked.connect(self.on_button_clicked)

        # Set window properties

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("MyWindow")

    def on_button_clicked(self):
        """Event method for the clicked signal"""
        QMessageBox.information(self, "Text", self.line_edit.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
