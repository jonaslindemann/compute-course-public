"""
What NOT to do: a long computation inside a slot freezes the user interface.

The clock label is updated by a QTimer every 100 ms. While the computation
runs, the event loop is blocked: the clock stops, the window cannot be
moved or redrawn and the operating system may report it as not responding.

Compare with threads_timer.py and threads_worker.py.
"""

import sys
import time

import numpy as np

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from qtpy.QtCore import QTimer

N_SAMPLES = 200_000_000
CHUNK_SIZE = 1_000_000


def estimate_pi(n_samples, chunk_size, rng):
    """Monte Carlo estimate of pi. Takes a few seconds."""
    inside = 0
    for _ in range(n_samples // chunk_size):
        x, y = rng.random((2, chunk_size))
        inside += np.count_nonzero(x * x + y * y <= 1.0)
    return 4.0 * inside / n_samples


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 120)
        self.move(50, 50)
        self.setWindowTitle("Frozen user interface")

        self.clock_label = QLabel()
        self.result_label = QLabel("Press Start")
        self.start_button = QPushButton("Start computation")

        layout = QVBoxLayout(self)
        layout.addWidget(self.clock_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.result_label)

        self.start_button.clicked.connect(self.on_start)

        # The clock shows whether the event loop is running

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(100)

    def update_clock(self):
        """Show the current time"""
        self.clock_label.setText(f"Clock: {time.strftime('%H:%M:%S')}.{int(time.time() * 10) % 10}")

    def on_start(self):
        """Run the computation directly in the slot - blocks the event loop"""

        # This text is never shown: the window is not repainted until the
        # slot returns.

        self.result_label.setText("Computing...")

        pi = estimate_pi(N_SAMPLES, CHUNK_SIZE, np.random.default_rng())

        self.result_label.setText(f"pi ≈ {pi:.6f}")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
