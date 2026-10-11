"""
A static line plot using pyqtgraph, embedded in a Qt window.
Requires the extra package "pyqtgraph".
"""

import sys

import pyqtgraph as pg

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout


class GraphWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.setWindowTitle("Graph Window")
        self.resize(800, 600)

        # Create plot widget

        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setLabel("bottom", "Time (min)")
        self.plot_graph.setLabel("left", "Temperature (°C)")

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_graph)

        # Plot data

        minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(minutes, temperature, pen=pg.mkPen("r", width=2))

        # Set fixed axis ranges and disable mouse interaction for a static view

        self.plot_graph.setXRange(min(minutes), max(minutes))
        self.plot_graph.setYRange(min(temperature) - 1, max(temperature) + 1)
        self.plot_graph.setMouseEnabled(x=False, y=False)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = GraphWindow()
    window.show()

    sys.exit(app.exec())
