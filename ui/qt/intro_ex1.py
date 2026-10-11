"""
A first Qt program. Shows that app.exec() blocks until the last window
has been closed.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget

if __name__ == "__main__":

    # Create application object

    app = QApplication(sys.argv)

    # Create user interface objects

    widget = QWidget()
    widget.resize(250, 150)
    widget.move(300, 300)
    widget.setWindowTitle("Hello Qt")
    widget.show()

    # Enter the event loop. exec() returns when the last window is closed.

    print("Before event loop.")
    exit_code = app.exec()
    print("Last window closed.")

    sys.exit(exit_code)
