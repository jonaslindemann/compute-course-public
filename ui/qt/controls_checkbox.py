"""
QCheckBox example.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QMessageBox


class MyWindow(QWidget):
    """Main window class for our application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 100)
        self.move(50, 50)
        self.setWindowTitle("Checkbox Example")

        # Create check box

        self.check_box = QCheckBox("Extra everything")
        self.check_box.setChecked(True)
        self.check_box.toggled.connect(self.on_toggled)

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.check_box)
        layout.addStretch()

    def on_toggled(self, checked):
        """Respond to the check box being toggled.

        Use isChecked()/toggled rather than checkState(). In Qt 6
        checkState() returns an enum which is always truthy.
        """
        if checked:
            QMessageBox.information(self, "Message", "Extra everything")
        else:
            QMessageBox.information(self, "Message", "Nothing extra")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
