"""
The smallest possible Qt application: an empty window and the event loop.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget

if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = QWidget()
    widget.show()

    sys.exit(app.exec())
