"""
Loading a user interface designed in Qt Designer (form.ui) at runtime.

Widgets in the .ui file become attributes named after their objectName.
"""

import sys
from pathlib import Path

from qtpy.QtWidgets import QApplication, QWidget
from qtpy import uic

HERE = Path(__file__).resolve().parent


class MainWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Load the .ui file relative to this script, not the working directory

        uic.loadUi(str(HERE / "form.ui"), self)

        self.push_button.setText("Press me!")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
