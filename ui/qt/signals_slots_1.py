"""
Signals and slots: connecting the clicked signal of a button to a method.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 100)
        self.move(50, 50)
        self.setWindowTitle("Signals and slots")

        # Create button and connect the clicked signal to our method (slot)

        self.button = QPushButton("Press")
        self.button.clicked.connect(self.on_button_clicked)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addStretch()

    def on_button_clicked(self):
        """Respond to button click"""
        QMessageBox.information(self, "Message", "Ouch!")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
