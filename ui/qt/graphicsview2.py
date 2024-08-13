#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:10:06 2017

@author: lindemann
"""

import sys
from random import uniform

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsView,
    QApplication,
    QGraphicsScene,
)

from qtpy.QtGui import QPen, QBrush, QColor, QPainter, QFont, QColor
from qtpy.QtCore import Qt


class DrawingEnv:
    """Drawing environment class"""

    def __init__(self):
        """Class constructor"""
        self.scene = QGraphicsScene()
        self.pen = QPen(Qt.black)
        self.pen.setWidth(3)
        self.no_pen = QPen(Qt.NoPen)
        self.brush = QBrush(Qt.red)
        self.empty_brush = QBrush(Qt.NoBrush)
        self.font = QFont("Arial", 22)

        self.current_brush = self.empty_brush
        self.current_pen = self.pen

    def line(self, x1, y1, x2, y2):
        """Draw a line"""
        self.scene.addLine(x1, y1, x2, y2, self.current_pen)

    def circle(self, x, y, r):
        """Draw a circle"""
        self.scene.addEllipse(
            x - r, y - r, 2 * r, 2 * r, self.current_pen, self.current_brush
        )

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
        """Sets the color used to fill shapes"""

        self.brush.setColor(QColor(int(red), int(green), int(blue), int(alpha)))
        self.current_brush = self.brush

    def no_fill(self):
        """Disables filling geometry"""
        self.current_brush = self.empty_brush

    def no_stroke(self):
        """Disables drawing the stroke (outline)"""
        self.current_pen = self.no_pen

    def stroke(self, red, green, blue, alpha=255):
        """Sets the color used to draw lines and borders around shapes"""
        self.pen.setColor(QColor(int(red), int(green), int(blue), int(alpha)))
        self.current_pen = self.pen

    def stroke_weight(self, weight):
        """Sets the width of the stroke used to draw lines and borders around shapes"""
        self.pen.setWidth(weight)


class GraphicsWindow(QWidget, DrawingEnv):
    """Main window class for the Flow application"""

    def __init__(self):
        """Class constructor"""
        super(GraphicsWindow, self).__init__()

        # Create view

        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setInteractive(True)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)

        # Draw some shapes

        for _ in range(100):
            self.stroke(uniform(0, 255), uniform(0, 255), uniform(0, 255))
            self.fill(uniform(0, 255), uniform(0, 255), uniform(0, 255))
            self.line(
                uniform(-1000.0, 1000.0),
                uniform(-1000.0, 1000.0),
                uniform(-1000.0, 1000.0),
                uniform(-1000.0, 1000.0),
            )
            self.rectangle(
                uniform(-1000.0, 1000.0),
                uniform(-1000.0, 1000.0),
                uniform(0.0, 100.0),
                uniform(0.0, 100.0),
            )
            self.circle(
                uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0), uniform(0.0, 100.0)
            )
            self.text(uniform(-1000.0, 1000.0), uniform(-1000.0, 1000.0), "Hello Qt!")

        # Set layout

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graphics_view)

        # Set window title and size

        self.setWindowTitle("Graphics View")
        self.resize(800, 800)

        # Show the view

        self.graphics_view.show()

    def showEvent(self, _):
        """Event handler for the show event"""
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphics_view.centerOn(0, 0)

    def resizeEvent(self, _):
        """Event handler for the resize event"""
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphics_view.centerOn(0, 0)


if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = GraphicsWindow()
    window.show()

    sys.exit(app.exec_())
