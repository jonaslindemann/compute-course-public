"""
Keeping the user interface responsive with a QTimer.

The computation is split into small steps. A QTimer with interval 0 calls
step() whenever the event loop is idle, so user input and repainting are
handled between the steps. No threads are needed, but the computation
must be possible to divide into short steps.

Compare with threads_frozen.py and threads_worker.py.
"""

import sys
import time

import numpy as np

from qtpy.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QProgressBar, QHBoxLayout, QVBoxLayout,
)
from qtpy.QtCore import QTimer

N_SAMPLES = 200_000_000
CHUNK_SIZE = 1_000_000


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 150)
        self.move(50, 50)
        self.setWindowTitle("Responsive with QTimer")

        # Computation state

        self.rng = np.random.default_rng()
        self.n_chunks = N_SAMPLES // CHUNK_SIZE
        self.chunk = 0
        self.inside = 0

        # Controls

        self.clock_label = QLabel()
        self.result_label = QLabel("Press Start")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.n_chunks)
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        buttons = QHBoxLayout()
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.clock_label)
        layout.addLayout(buttons)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_label)

        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)

        # Timer driving the computation. Interval 0 = run when idle.

        self.compute_timer = QTimer(self)
        self.compute_timer.setInterval(0)
        self.compute_timer.timeout.connect(self.step)

        # The clock shows whether the event loop is running

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(100)

    def update_clock(self):
        """Show the current time"""
        self.clock_label.setText(f"Clock: {time.strftime('%H:%M:%S')}.{int(time.time() * 10) % 10}")

    def on_start(self):
        """Reset the computation and start the timer"""
        self.chunk = 0
        self.inside = 0
        self.progress_bar.setValue(0)
        self.result_label.setText("Computing...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.compute_timer.start()

    def on_stop(self):
        """Stop the computation"""
        self.compute_timer.stop()
        self.result_label.setText("Stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def step(self):
        """Process one chunk. Must return quickly (a few ms)."""

        x, y = self.rng.random((2, CHUNK_SIZE))
        self.inside += np.count_nonzero(x * x + y * y <= 1.0)
        self.chunk += 1
        self.progress_bar.setValue(self.chunk)

        if self.chunk == self.n_chunks:
            self.compute_timer.stop()
            self.result_label.setText(f"pi ≈ {4.0 * self.inside / N_SAMPLES:.6f}")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
