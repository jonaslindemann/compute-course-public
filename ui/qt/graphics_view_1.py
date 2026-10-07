"""
QGraphicsView/QGraphicsScene loaded from a Qt Designer file, drawing
random lines that are kept fitted to the view.
"""

import sys
from pathlib import Path
from random import uniform

from qtpy.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from qtpy.QtGui import QPainter, QPen
from qtpy.QtCore import Qt
from qtpy import uic

HERE = Path(__file__).resolve().parent


class MainWindow(QMainWindow):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Load the user interface. Creates self.graphics_view.

        uic.loadUi(str(HERE / "graphics_view_1.ui"), self)

        # Create a scene and connect it to the view

        self.scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setInteractive(True)
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw random lines

        pen = QPen(Qt.GlobalColor.red)

        for _ in range(100):
            self.scene.addLine(
                uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0),
                uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0),
                pen,
            )

        self.resize(800, 800)

    def fit_scene(self):
        """Fit the whole scene in the view"""
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def showEvent(self, event):
        """Called when the window is shown"""
        super().showEvent(event)
        self.fit_scene()

    def resizeEvent(self, event):
        """Called when the window is resized"""
        super().resizeEvent(event)
        self.fit_scene()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
