import sys

import pyqtgraph as pg

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
)

from qtpy.QtGui import QPen, QBrush, QColor, QPainter, QFont, QColor
from qtpy.QtCore import Qt


class GraphWindowe(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Window")
        self.resize(800, 800)

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.plot_graph)

        minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(minutes, temperature)


if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = GraphWindowe()
    window.show()

    sys.exit(app.exec_())
