"""
QSlider example with a vertical and a horizontal slider.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QSlider, QHBoxLayout
from qtpy.QtCore import Qt


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        # Configure window

        self.resize(300, 200)
        self.move(50, 50)
        self.setWindowTitle("Slider Example")

        # Create controls

        self.vert_slider = QSlider(Qt.Orientation.Vertical)
        self.vert_slider.setRange(0, 100)
        self.vert_slider.setValue(50)

        self.horiz_slider = QSlider(Qt.Orientation.Horizontal)
        self.horiz_slider.setRange(0, 100)
        self.horiz_slider.setValue(50)
        self.horiz_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horiz_slider.setTickInterval(10)

        # Connect signals

        self.vert_slider.valueChanged.connect(self.on_value_changed)
        self.horiz_slider.valueChanged.connect(self.on_value_changed)

        # Layout

        layout = QHBoxLayout(self)
        layout.addWidget(self.vert_slider)
        layout.addWidget(self.horiz_slider, 0, Qt.AlignmentFlag.AlignTop)

    def on_value_changed(self, value):
        """Handle the valueChanged signal"""
        print("vertical value   =", self.vert_slider.value())
        print("horizontal value =", self.horiz_slider.value())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
