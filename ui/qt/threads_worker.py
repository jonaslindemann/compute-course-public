"""
Running a long computation in a worker thread.

The worker object is moved to a QThread and communicates with the user
interface only through signals. Signals emitted from the worker thread
are delivered as events in the GUI thread, so the slots can safely
update widgets.

Golden rule: never touch widgets from the worker thread.

Compare with threads_frozen.py and threads_timer.py.
"""

import sys
import time

import numpy as np

from qtpy.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QProgressBar, QHBoxLayout, QVBoxLayout,
)
from qtpy.QtCore import QObject, QThread, QTimer, Signal

N_SAMPLES = 200_000_000
CHUNK_SIZE = 1_000_000


class PiWorker(QObject):
    """Monte Carlo estimate of pi. Runs in a separate thread."""

    progress = Signal(int)      # Percent done
    finished = Signal(float)    # Result
    cancelled = Signal()

    def __init__(self, n_samples, chunk_size):
        super().__init__()
        self.n_samples = n_samples
        self.chunk_size = chunk_size

    def run(self):
        """Do the computation. Called in the worker thread."""

        rng = np.random.default_rng()
        n_chunks = self.n_samples // self.chunk_size
        inside = 0

        for chunk in range(n_chunks):

            # Check if the GUI has asked us to stop

            if QThread.currentThread().isInterruptionRequested():
                self.cancelled.emit()
                return

            x, y = rng.random((2, self.chunk_size))
            inside += np.count_nonzero(x * x + y * y <= 1.0)

            self.progress.emit(100 * (chunk + 1) // n_chunks)

        self.finished.emit(4.0 * inside / self.n_samples)


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(300, 150)
        self.move(50, 50)
        self.setWindowTitle("Responsive with a worker thread")

        self.worker_thread = None
        self.worker = None

        # Controls

        self.clock_label = QLabel()
        self.result_label = QLabel("Press Start")
        self.progress_bar = QProgressBar()
        self.start_button = QPushButton("Start")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)

        buttons = QHBoxLayout()
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.clock_label)
        layout.addLayout(buttons)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_label)

        self.start_button.clicked.connect(self.on_start)
        self.cancel_button.clicked.connect(self.on_cancel)

        # The clock shows whether the event loop is running

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(100)

    def update_clock(self):
        """Show the current time"""
        self.clock_label.setText(f"Clock: {time.strftime('%H:%M:%S')}.{int(time.time() * 10) % 10}")

    def on_start(self):
        """Create a worker and a thread and start the computation"""

        self.worker_thread = QThread()
        self.worker = PiWorker(N_SAMPLES, CHUNK_SIZE)
        self.worker.moveToThread(self.worker_thread)

        # Start the work when the thread starts

        self.worker_thread.started.connect(self.worker.run)

        # Worker -> GUI. These slots run in the GUI thread.

        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.cancelled.connect(self.on_cancelled)

        # Stop the thread's event loop when the worker is done

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.cancelled.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.on_thread_finished)

        self.progress_bar.setValue(0)
        self.result_label.setText("Computing...")
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        self.worker_thread.start()

    def on_cancel(self):
        """Ask the worker to stop. It checks the flag between chunks."""
        if self.worker_thread is not None:
            self.worker_thread.requestInterruption()

    def on_finished(self, pi):
        """Called when the worker has a result"""
        self.result_label.setText(f"pi ≈ {pi:.6f}")

    def on_cancelled(self):
        """Called when the worker has stopped early"""
        self.result_label.setText("Cancelled")

    def on_thread_finished(self):
        """Called when the thread has stopped. Release worker and thread."""
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.worker.deleteLater()
        self.worker_thread.deleteLater()
        self.worker = None
        self.worker_thread = None

    def closeEvent(self, event):
        """Stop the thread before the window is destroyed"""
        if self.worker_thread is not None:
            self.worker_thread.requestInterruption()
            self.worker_thread.quit()
            self.worker_thread.wait()
        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
