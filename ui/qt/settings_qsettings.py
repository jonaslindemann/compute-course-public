"""
Remembering settings between sessions with QSettings.

QSettings stores values in the platform's native location: the registry
on Windows, a .plist file on macOS and an .ini file on Linux. Here we
remember the window geometry, the last used directory and two parameters.

Run the program, change the values, close it and start it again.
"""

import sys
from pathlib import Path

from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDoubleSpinBox, QSpinBox, QLabel,
    QPushButton, QFormLayout, QVBoxLayout, QFileDialog,
)
from qtpy.QtCore import QSettings


class MyWindow(QMainWindow):
    """Main window class"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.setWindowTitle("QSettings Example")

        # Organisation and application name decide where settings are stored

        self.settings = QSettings("ComputeCourse", "QtExamples")

        # Controls

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.1, 100.0)
        self.length_spin.setSuffix(" m")

        self.points_spin = QSpinBox()
        self.points_spin.setRange(2, 1000)

        self.open_button = QPushButton("Open file...")
        self.file_label = QLabel("No file selected")

        # Layout

        form = QFormLayout()
        form.addRow("Length", self.length_spin)
        form.addRow("Points", self.points_spin)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addLayout(form)
        layout.addWidget(self.open_button)
        layout.addWidget(self.file_label)
        layout.addStretch()
        self.setCentralWidget(central)

        self.open_button.clicked.connect(self.on_open)

        # Restore settings. The type argument converts the stored value,
        # which may come back as a string on some platforms.

        geometry = self.settings.value("window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        else:
            self.resize(300, 180)

        self.length_spin.setValue(self.settings.value("params/length", 3.0, type=float))
        self.points_spin.setValue(self.settings.value("params/points", 30, type=int))
        self.last_dir = self.settings.value("files/last_dir", str(Path.home()), type=str)

    def on_open(self):
        """Select a file, starting in the last used directory"""

        filename, _ = QFileDialog.getOpenFileName(self, "Open file", self.last_dir)

        if filename:
            self.last_dir = str(Path(filename).parent)
            self.file_label.setText(filename)

    def closeEvent(self, event):
        """Save settings when the window is closed"""

        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("params/length", self.length_spin.value())
        self.settings.setValue("params/points", self.points_spin.value())
        self.settings.setValue("files/last_dir", self.last_dir)

        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
