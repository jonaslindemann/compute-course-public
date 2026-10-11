"""
QLabel example: text labels and a label showing an image.
"""

import sys
from pathlib import Path

from qtpy.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox,
)
from qtpy.QtGui import QPixmap

HERE = Path(__file__).resolve().parent


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Configure window

        self.resize(400, 200)
        self.move(50, 50)
        self.setWindowTitle("Label Example")

        # Create controls

        self.label = QLabel("Text box")
        self.line_edit = QLineEdit("Text")
        self.button = QPushButton("Press")
        self.button.clicked.connect(self.on_button_clicked)

        # Create label control with an image

        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(300, 100)
        self.image_label.setPixmap(QPixmap(str(HERE / "python_logo.png")))

        # Layout

        row = QHBoxLayout()
        row.addWidget(self.label)
        row.addWidget(self.line_edit)
        row.addWidget(self.button)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self.image_label)
        layout.addStretch()

    def on_button_clicked(self):
        """Event method for the clicked signal"""
        QMessageBox.information(self, "Text", self.line_edit.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
