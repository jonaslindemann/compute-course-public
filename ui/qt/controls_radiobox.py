"""
QRadioButton example. Radio buttons with the same parent are mutually
exclusive.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 100)
        self.move(50, 50)
        self.setWindowTitle("Radio Button Example")

        # Create radio buttons

        self.radio_button1 = QRadioButton("Extra everything")
        self.radio_button2 = QRadioButton("Nothing extra")
        self.radio_button1.setChecked(True)

        self.radio_button1.clicked.connect(self.on_radio_button_clicked)
        self.radio_button2.clicked.connect(self.on_radio_button_clicked)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addStretch()

    def on_radio_button_clicked(self):
        """Respond to radio button selection"""
        if self.radio_button1.isChecked():
            QMessageBox.information(self, "Message", "Radio 1 selected")
        else:
            QMessageBox.information(self, "Message", "Radio 2 selected")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
