"""
A Processing-style drawing API (line, circle, fill, stroke ...) on top of
QGraphicsScene, shown in a QGraphicsView.
"""

import sys
from random import uniform

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from qtpy.QtGui import QPen, QBrush, QColor, QPainter, QFont
from qtpy.QtCore import Qt


class DrawingEnv:
    """Drawing environment wrapping a QGraphicsScene"""

    def __init__(self):
        """Class constructor"""
        self.scene = QGraphicsScene()
        self.pen = QPen(Qt.GlobalColor.black)
        self.pen.setWidth(3)
        self.no_pen = QPen(Qt.PenStyle.NoPen)
        self.brush = QBrush(Qt.GlobalColor.red)
        self.empty_brush = QBrush(Qt.BrushStyle.NoBrush)
        self.font = QFont("Arial", 22)

        self.current_brush = self.empty_brush
        self.current_pen = self.pen

    def line(self, x1, y1, x2, y2):
        """Draw a line"""
        self.scene.addLine(x1, y1, x2, y2, self.current_pen)

    def circle(self, x, y, r):
        """Draw a circle"""
        self.scene.addEllipse(x - r, y - r, 2 * r, 2 * r, self.current_pen, self.current_brush)

    def rectangle(self, x, y, w, h):
        """Draw a rectangle"""
        self.scene.addRect(x, y, w, h, self.current_pen, self.current_brush)

    def text(self, x, y, text):
        """Draw text"""
        self.scene.addText(text, self.font).setPos(x, y)

    def font_size(self, size):
        """Set the font size"""
        self.font.setPointSize(size)

    def clear(self):
        """Clear the scene"""
        self.scene.clear()

    def fill(self, red, green, blue, alpha=255):
        """Set the color used to fill shapes"""
        self.brush.setColor(QColor(int(red), int(green), int(blue), int(alpha)))
        self.current_brush = self.brush

    def no_fill(self):
        """Disable filling of shapes"""
        self.current_brush = self.empty_brush

    def no_stroke(self):
        """Disable drawing of outlines"""
        self.current_pen = self.no_pen

    def stroke(self, red, green, blue, alpha=255):
        """Set the color used for lines and outlines"""
        self.pen.setColor(QColor(int(red), int(green), int(blue), int(alpha)))
        self.current_pen = self.pen

    def stroke_weight(self, weight):
        """Set the width of lines and outlines"""
        self.pen.setWidth(weight)


class GraphicsWindow(QWidget):
    """Main window class. Uses a DrawingEnv to draw random shapes."""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.draw = DrawingEnv()

        # Create view

        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(self.draw.scene)
        self.graphics_view.setInteractive(True)
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw some shapes

        d = self.draw

        for _ in range(100):
            d.stroke(uniform(0, 255), uniform(0, 255), uniform(0, 255))
            d.fill(uniform(0, 255), uniform(0, 255), uniform(0, 255))
            d.line(uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0),
                   uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0))
            d.rectangle(uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0),
                        uniform(0.0, 100.0), uniform(0.0, 100.0))
            d.circle(uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0), uniform(0.0, 100.0))
            d.text(uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0), "Hello Qt!")

        # Layout

        layout = QVBoxLayout(self)
        layout.addWidget(self.graphics_view)

        # Set window title and size

        self.setWindowTitle("Graphics View")
        self.resize(800, 800)

    def fit_scene(self):
        """Fit the whole scene in the view"""
        self.graphics_view.fitInView(self.draw.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

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

    window = GraphicsWindow()
    window.show()

    sys.exit(app.exec())
