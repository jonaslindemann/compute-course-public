import sys

import pyqtgraph as pg

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
)

from qtpy.QtGui import QPen, QBrush, QColor, QPainter, QFont, QColor
from qtpy.QtCore import Qt



# Fixed class name and static plot configuration
class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Window")
        self.resize(800, 800)

        self.plot_graph = pg.PlotWidget()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.plot_graph)

        minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(minutes, temperature, pen=pg.mkPen('r', width=2))

        # Set fixed axis ranges
        self.plot_graph.setXRange(min(minutes), max(minutes))
        self.plot_graph.setYRange(min(temperature) - 1, max(temperature) + 1)

        # Optionally disable mouse interaction for a static view
        self.plot_graph.setMouseEnabled(x=False, y=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
