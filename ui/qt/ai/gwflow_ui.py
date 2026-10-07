"""
Groundwater flow application

A Qt user interface for GroundwaterModel. The model is solved in a worker
thread so the window stays responsive while meshing and solving.

Corrected version of generated/gwflow_ui.py. See review.md.
"""

import sys

import numpy as np

from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDockWidget, QFormLayout, QVBoxLayout,
    QDoubleSpinBox, QLineEdit, QPushButton, QComboBox, QProgressBar, QMessageBox,
)
from qtpy.QtGui import QDoubleValidator
from qtpy.QtCore import Qt, QObject, QThread, QLocale, Signal

from matplotlib.figure import Figure
from matplotlib.collections import PolyCollection
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

import calfem.vis_mpl as cfv

from gwflow_model import GroundwaterModel


class SolveWorker(QObject):
    """Solves the model in a separate thread"""

    finished = Signal()
    failed = Signal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        """Solve the model. Called in the worker thread."""
        try:
            self.model.solve()
        except Exception as e:
            self.failed.emit(str(e))
            return
        self.finished.emit()


class GroundwaterWindow(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Groundwater flow")
        self.resize(1200, 700)

        self.model = GroundwaterModel()
        self.worker_thread = None
        self.worker = None

        # Plot area

        self.figure = Figure(layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.addWidget(self.toolbar)
        central_layout.addWidget(self.canvas)
        self.setCentralWidget(central)

        # Parameter inputs

        self.w_spin = self.create_spin(10.0, 500.0, 1, " m")
        self.h_spin = self.create_spin(1.0, 100.0, 1, " m")
        self.t_spin = self.create_spin(0.5, 50.0, 1, " m")
        self.d_spin = self.create_spin(0.5, 50.0, 1, " m")
        # Permeabilities of soils span many orders of magnitude (1e-10 to
        # 1e-2 m/s), which a spin box with fixed decimals cannot represent.

        self.kx_edit = self.create_scientific_edit()
        self.ky_edit = self.create_scientific_edit()
        self.head_left_spin = self.create_spin(0.0, 100.0, 1, " m")
        self.head_right_spin = self.create_spin(0.0, 100.0, 1, " m")
        self.el_size_spin = self.create_spin(0.1, 5.0, 2, "")

        self.result_combo = QComboBox()
        self.result_combo.addItems(["Head", "Flow"])

        self.solve_button = QPushButton("Solve")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        form = QFormLayout()
        form.addRow("Width w", self.w_spin)
        form.addRow("Height h", self.h_spin)
        form.addRow("Notch width t", self.t_spin)
        form.addRow("Notch depth d", self.d_spin)
        form.addRow("Permeability kx (m/s)", self.kx_edit)
        form.addRow("Permeability ky (m/s)", self.ky_edit)
        form.addRow("Head left", self.head_left_spin)
        form.addRow("Head right", self.head_right_spin)
        form.addRow("Element size factor", self.el_size_spin)
        form.addRow("Show", self.result_combo)

        self.panel = QWidget()
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.addLayout(form)
        panel_layout.addWidget(self.solve_button)
        panel_layout.addWidget(self.progress_bar)
        panel_layout.addStretch()

        self.dock = QDockWidget("Parameters", self)
        self.dock.setWidget(self.panel)
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        # Signals

        self.solve_button.clicked.connect(self.on_solve)
        self.result_combo.currentIndexChanged.connect(self.draw_results)

        self.update_controls()

    def create_spin(self, minimum, maximum, decimals, suffix):
        """Create a configured QDoubleSpinBox"""
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum)
        spin.setDecimals(decimals)
        spin.setSuffix(suffix)
        return spin

    def create_scientific_edit(self):
        """Create a QLineEdit accepting positive numbers in scientific notation"""
        validator = QDoubleValidator(1e-15, 1e6, 15, self)
        validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        validator.setLocale(QLocale.c())
        edit = QLineEdit()
        edit.setValidator(validator)
        return edit

    def update_controls(self):
        """Model -> controls"""
        self.w_spin.setValue(self.model.w)
        self.h_spin.setValue(self.model.h)
        self.t_spin.setValue(self.model.t)
        self.d_spin.setValue(self.model.d)
        self.kx_edit.setText(f"{self.model.kx:g}")
        self.ky_edit.setText(f"{self.model.ky:g}")
        self.head_left_spin.setValue(self.model.head_left)
        self.head_right_spin.setValue(self.model.head_right)
        self.el_size_spin.setValue(self.model.el_size_factor)

    def update_model(self):
        """Controls -> model"""
        self.model.w = self.w_spin.value()
        self.model.h = self.h_spin.value()
        self.model.t = self.t_spin.value()
        self.model.d = self.d_spin.value()
        # Incomplete input such as "1e-" keeps the previous model value

        if self.kx_edit.hasAcceptableInput():
            self.model.kx = float(self.kx_edit.text())
        if self.ky_edit.hasAcceptableInput():
            self.model.ky = float(self.ky_edit.text())
        self.model.head_left = self.head_left_spin.value()
        self.model.head_right = self.head_right_spin.value()
        self.model.el_size_factor = self.el_size_spin.value()

    def on_solve(self):
        """Start solving in a worker thread"""

        self.update_model()
        self.update_controls()

        # Check the parameters here, in the GUI thread. Invalid geometry can
        # make Gmsh hang, and a hung worker thread cannot be stopped.

        try:
            self.model.validate()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return

        self.worker_thread = QThread()
        self.worker = SolveWorker(self.model)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_solved)
        self.worker.failed.connect(self.on_failed)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.failed.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.on_thread_finished)

        self.panel.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.statusBar().showMessage("Solving...")

        self.worker_thread.start()

    def on_solved(self):
        """Called when the model has been solved"""
        self.statusBar().showMessage(
            f"{self.model.edof.shape[0]} elements, total flow {self.model.total_flow:.4g}"
        )
        self.draw_results()

    def on_failed(self, message):
        """Called if solving failed"""
        self.statusBar().showMessage("Solve failed")
        QMessageBox.critical(self, "Solve failed", message)

    def on_thread_finished(self):
        """Clean up the worker and thread"""
        self.panel.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.worker.deleteLater()
        self.worker_thread.deleteLater()
        self.worker = None
        self.worker_thread = None

    def draw_results(self):
        """Draw the selected result"""

        if self.model.a is None:
            return

        self.figure.clear()
        ax = self.figure.add_subplot()

        if self.result_combo.currentText() == "Head":
            mappable = cfv.draw_nodal_values(
                self.model.a, self.model.coords, self.model.edof, 1, 3,
                axes=ax, draw_elements=False, title="Head (m)",
            )
        else:
            # cfv.draw_element_values() has no axes argument and draws on the
            # current pyplot axes, not on our embedded figure. Draw the
            # element values directly instead.
            polygons = np.stack([self.model.ex, self.model.ey], axis=2)
            mappable = PolyCollection(polygons, array=self.model.flow, edgecolors="face")
            ax.add_collection(mappable)
            ax.autoscale_view()
            ax.set_title("Flow magnitude")

        self.figure.colorbar(mappable, ax=ax, orientation="horizontal")
        ax.set_aspect("equal")
        self.canvas.draw_idle()

    def closeEvent(self, event):
        """Wait for a running solve before closing"""
        if self.worker_thread is not None:
            self.worker_thread.quit()
            self.worker_thread.wait()
        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = GroundwaterWindow()
    window.show()

    sys.exit(app.exec())
