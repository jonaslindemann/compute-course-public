"""
Embedding a matplotlib figure in a Qt window, updated from a slider.

FigureCanvasQTAgg is a QWidget, so it can be placed in any layout.
The plot is updated by changing the data of the existing line and
calling draw_idle(), which is much faster than clearing and replotting.
"""

import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from qtpy.QtWidgets import (
    QApplication, QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout,
)
from qtpy.QtCore import Qt


class PlotWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(800, 600)
        self.move(50, 50)
        self.setWindowTitle("Matplotlib in Qt")

        # Create the figure and canvas. Use matplotlib.figure.Figure, not
        # pyplot, so that pyplot does not create windows of its own.

        self.figure = Figure(layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.ax = self.figure.add_subplot()
        self.x = np.linspace(0.0, 10.0, 500)
        (self.line,) = self.ax.plot(self.x, self.damped_wave(1.0))
        self.ax.set_xlabel("t (s)")
        self.ax.set_ylabel("y")
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.grid(True)

        # Slider for the frequency. QSlider only handles integers, so
        # slider value 10 corresponds to 1.0 Hz.

        self.freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_slider.setRange(1, 50)
        self.freq_slider.setValue(10)
        self.freq_label = QLabel()

        # Layout

        slider_row = QHBoxLayout()
        slider_row.addWidget(QLabel("Frequency"))
        slider_row.addWidget(self.freq_slider)
        slider_row.addWidget(self.freq_label)

        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(slider_row)

        # Connect signals

        self.freq_slider.valueChanged.connect(self.on_frequency_changed)
        self.on_frequency_changed(self.freq_slider.value())

    def damped_wave(self, frequency):
        """Return a damped sine wave sampled at self.x"""
        return np.exp(-0.2 * self.x) * np.sin(2.0 * np.pi * frequency * self.x)

    def on_frequency_changed(self, value):
        """Update the plot for a new frequency"""
        frequency = value / 10.0
        self.freq_label.setText(f"{frequency:.1f} Hz")
        self.line.set_ydata(self.damped_wave(frequency))
        self.canvas.draw_idle()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PlotWindow()
    window.show()

    sys.exit(app.exec())
