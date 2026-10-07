"""
QComboBox example.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Configure window

        self.resize(300, 100)
        self.move(50, 50)
        self.setWindowTitle("ComboBox Example")

        # Create combobox control and add options

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Alternative 1", "Alternative 2", "Alternative 3", "Alternative 4"])

        # Set default selection

        self.combo_box.setCurrentIndex(3)

        # Connect event method to signal

        self.combo_box.currentIndexChanged.connect(self.on_current_index_changed)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.combo_box)
        layout.addStretch()

    def on_current_index_changed(self, index):
        """Handle the currentIndexChanged signal"""
        QMessageBox.information(
            self, "Message", f"You selected index {index}: {self.combo_box.currentText()}"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
