#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Volume Explorer

A companion to surface_explorer.py and particle_explorer.py: an interactive
PyVista/Qt application that visualises a 3D scalar field (see
volume_functions.py) using two independently positionable cutting planes,
plus an optional experimental direct volume rendering mode.

Requires the extra packages "pyvista" and "pyvistaqt".

@author: Jonas Lindemann
"""

import os
import sys

import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor

from qtpy.QtWidgets import (
    QMainWindow, QApplication, QWidget, QDockWidget, QVBoxLayout,
    QFormLayout, QHBoxLayout, QGroupBox, QComboBox, QCheckBox, QSlider,
    QLabel, QAction, QFileDialog, QMessageBox,
)
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QIcon

import volume_functions as vf

ICON_DIR = os.path.dirname(os.path.abspath(__file__))

AXIS_NORMALS = {
    "X": (1.0, 0.0, 0.0),
    "Y": (0.0, 1.0, 0.0),
    "Z": (0.0, 0.0, 1.0),
}


def icon(name):
    """Load one of the icons8-*.png icons shipped in this folder"""
    return QIcon(os.path.join(ICON_DIR, name))


class LabeledSlider(QWidget):
    """A horizontal slider with a name label and a live numeric value label.

    QSlider only works with integers, so float ranges are internally
    scaled by 10**decimals.
    """

    valueChanged = Signal(float)

    def __init__(self, name, minimum, maximum, default, decimals=1, parent=None):
        super().__init__(parent)

        self._scale = 10 ** decimals
        self._decimals = decimals

        self.name_label = QLabel(name)
        self.name_label.setMinimumWidth(90)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(round(minimum * self._scale)))
        self.slider.setMaximum(int(round(maximum * self._scale)))
        self.slider.setValue(int(round(default * self._scale)))

        self.value_label = QLabel(f"{default:.{decimals}f}")
        self.value_label.setMinimumWidth(48)
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.name_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)

        self.slider.valueChanged.connect(self._on_slider_changed)

    def _on_slider_changed(self, raw_value):
        value = raw_value / self._scale
        self.value_label.setText(f"{value:.{self._decimals}f}")
        self.valueChanged.emit(value)

    def value(self):
        return self.slider.value() / self._scale

    def set_range(self, minimum, maximum):
        """Change the slider's range in place, clamping the current value"""

        clamped = max(minimum, min(maximum, self.value()))

        self.slider.blockSignals(True)
        self.slider.setMinimum(int(round(minimum * self._scale)))
        self.slider.setMaximum(int(round(maximum * self._scale)))
        self.slider.setValue(int(round(clamped * self._scale)))
        self.slider.blockSignals(False)

        self.value_label.setText(f"{clamped:.{self._decimals}f}")


class CuttingPlanePanel(QGroupBox):
    """Controls for one axis-aligned cutting plane: enabled, axis and position"""

    changed = Signal()

    def __init__(self, title, default_axis, extent, parent=None):
        super().__init__(title, parent)

        layout = QVBoxLayout(self)

        self.enabled_checkbox = QCheckBox("Show")
        self.enabled_checkbox.setChecked(True)
        self.enabled_checkbox.stateChanged.connect(lambda _: self.changed.emit())

        self.axis_combo = QComboBox()
        self.axis_combo.addItems(["X", "Y", "Z"])
        self.axis_combo.setCurrentText(default_axis)
        self.axis_combo.currentTextChanged.connect(lambda _: self.changed.emit())

        self.position_slider = LabeledSlider("Position", -extent, extent, 0.0, decimals=2)
        self.position_slider.valueChanged.connect(lambda _: self.changed.emit())

        axis_form = QFormLayout()
        axis_form.addRow(self.enabled_checkbox, self.axis_combo)

        layout.addLayout(axis_form)
        layout.addWidget(self.position_slider)

    def set_extent(self, extent):
        self.position_slider.set_range(-extent, extent)

    @property
    def enabled(self):
        return self.enabled_checkbox.isChecked()

    @property
    def axis(self):
        return self.axis_combo.currentText()

    @property
    def position(self):
        return self.position_slider.value()

    def normal_and_origin(self):
        normal = AXIS_NORMALS[self.axis]
        origin = tuple(p * n for p, n in zip((self.position,) * 3, normal))
        return normal, origin


class VolumeExplorerWindow(QMainWindow):
    """Main window for the Volume Explorer application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(1200, 800)
        self.move(50, 50)
        self.setWindowTitle("Volume Explorer")

        self.function_name = next(iter(vf.VOLUME_FUNCTIONS))
        self.param_sliders = {}
        self.grid = None
        self.box_actor = None
        self.plane_actors = [None, None]
        self.volume_actor = None

        # Create the 3D view and the docked control panel

        # 3D view

        self.plotter = QtInteractor(self)
        self.setCentralWidget(self.plotter)

        # Docked control panel

        self.dock = QDockWidget("Controls", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        panel = QWidget()
        controls_layout = QVBoxLayout(panel)

        # Function selector and parameters

        self.function_combo = QComboBox()
        self.function_combo.addItems(vf.VOLUME_FUNCTIONS.keys())
        self.function_combo.currentTextChanged.connect(self.on_function_changed)

        function_form = QFormLayout()
        function_form.addRow("Function", self.function_combo)
        controls_layout.addLayout(function_form)

        self.param_group = QGroupBox("Function parameters")
        self.param_layout = QVBoxLayout(self.param_group)
        controls_layout.addWidget(self.param_group)

        # Grid

        self.grid_group = QGroupBox("Grid")
        grid_layout = QVBoxLayout(self.grid_group)
        self.resolution_slider = LabeledSlider("Resolution", 10, 90, 40, decimals=0)
        self.extent_slider = LabeledSlider("Extent", 1.0, 10.0, 4.0, decimals=1)
        self.resolution_slider.valueChanged.connect(lambda _: self.update_volume())
        self.extent_slider.valueChanged.connect(self.on_extent_changed)
        grid_layout.addWidget(self.resolution_slider)
        grid_layout.addWidget(self.extent_slider)
        controls_layout.addWidget(self.grid_group)

        # Cutting planes

        extent = self.extent_slider.value()
        self.plane_panels = [
            CuttingPlanePanel("Cutting plane 1", "X", extent),
            CuttingPlanePanel("Cutting plane 2", "Y", extent),
        ]
        for panel_widget in self.plane_panels:
            panel_widget.changed.connect(lambda: self.update_volume())
            controls_layout.addWidget(panel_widget)

        # Appearance

        self.appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(self.appearance_group)

        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["viridis", "plasma", "coolwarm", "turbo", "jet", "rainbow"])
        self.colormap_combo.currentTextChanged.connect(lambda _: self.update_volume())

        self.slice_opacity_slider = LabeledSlider("Slice opacity", 0.1, 1.0, 1.0, decimals=2)
        self.slice_opacity_slider.valueChanged.connect(lambda _: self.update_volume())

        self.box_checkbox = QCheckBox("Show bounding box")
        self.box_checkbox.setChecked(True)
        self.box_checkbox.stateChanged.connect(lambda _: self.update_volume())

        self.volume_checkbox = QCheckBox("Show volume (experimental)")
        self.volume_checkbox.stateChanged.connect(lambda _: self.update_volume())

        self.volume_opacity_slider = LabeledSlider("Volume opacity", 0.01, 0.5, 0.1, decimals=2)
        self.volume_opacity_slider.valueChanged.connect(lambda _: self.update_volume())

        appearance_layout.addRow("Colormap", self.colormap_combo)
        appearance_layout.addRow(self.slice_opacity_slider)
        appearance_layout.addRow(self.box_checkbox)
        appearance_layout.addRow(self.volume_checkbox)
        appearance_layout.addRow(self.volume_opacity_slider)

        controls_layout.addWidget(self.appearance_group)
        controls_layout.addStretch()

        self.dock.setWidget(panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.status_bar = self.statusBar()

        # Create menu bar and toolbar actions

        self.screenshot_action = QAction(icon("icons8-save.png"), "Save Screenshot...", self)
        self.screenshot_action.setShortcut("Ctrl+S")
        self.screenshot_action.triggered.connect(self.on_save_screenshot)

        self.export_action = QAction(icon("icons8-save-as.png"), "Export Volume...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self.on_export_volume)

        self.exit_action = QAction(icon("icons8-exit.png"), "Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)

        self.reset_camera_action = QAction("Reset Camera", self)
        self.reset_camera_action.setShortcut("Ctrl+R")
        self.reset_camera_action.triggered.connect(self.on_reset_camera)

        self.iso_view_action = QAction("Isometric View", self)
        self.iso_view_action.triggered.connect(lambda: self.plotter.view_isometric())

        self.top_view_action = QAction("Top View", self)
        self.top_view_action.triggered.connect(lambda: self.plotter.view_xy())

        self.front_view_action = QAction("Front View", self)
        self.front_view_action.triggered.connect(lambda: self.plotter.view_xz())

        self.about_action = QAction("About...", self)
        self.about_action.triggered.connect(self.on_about)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.screenshot_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.reset_camera_action)
        view_menu.addSeparator()
        view_menu.addAction(self.iso_view_action)
        view_menu.addAction(self.top_view_action)
        view_menu.addAction(self.front_view_action)
        view_menu.addSeparator()
        view_menu.addAction(self.dock.toggleViewAction())

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.about_action)

        toolbar = self.addToolBar("Main")
        toolbar.addAction(self.screenshot_action)
        toolbar.addAction(self.export_action)
        toolbar.addSeparator()
        toolbar.addAction(self.reset_camera_action)
        toolbar.addSeparator()
        toolbar.addAction(self.exit_action)

    # --- Parameter controls ------------------------------------------------

        self.rebuild_param_controls()
        self.update_volume(reset_camera=True)

    def rebuild_param_controls(self):
        """Rebuild the sliders for the currently selected function's parameters"""

        while self.param_layout.count():
            item = self.param_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.param_sliders = {}
        volume_function = vf.VOLUME_FUNCTIONS[self.function_name]

        for param_name, (minimum, maximum, default, decimals) in volume_function.params.items():
            slider = LabeledSlider(param_name.replace("_", " ").capitalize(), minimum, maximum, default, decimals)
            slider.valueChanged.connect(lambda _: self.update_volume())
            self.param_layout.addWidget(slider)
            self.param_sliders[param_name] = slider

    def on_function_changed(self, name):
        self.function_name = name
        self.rebuild_param_controls()
        self.update_volume(reset_camera=True)

    def on_extent_changed(self, extent):
        for panel_widget in self.plane_panels:
            panel_widget.set_extent(extent)
        self.update_volume()

    def current_param_values(self):
        return {name: slider.value() for name, slider in self.param_sliders.items()}

    # --- Scene construction --------------------------------------------------

    def build_grid(self):
        """Evaluate the current function on a regular 3D grid and wrap it as a pv.ImageData"""

        resolution = max(4, int(self.resolution_slider.value()))
        extent = self.extent_slider.value()

        axis = np.linspace(-extent, extent, resolution)
        X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")

        volume_function = vf.VOLUME_FUNCTIONS[self.function_name]
        values = volume_function.evaluate(X, Y, Z, self.current_param_values())

        grid = pv.ImageData()
        grid.dimensions = (resolution, resolution, resolution)
        grid.origin = (-extent, -extent, -extent)
        spacing = 2 * extent / (resolution - 1)
        grid.spacing = (spacing, spacing, spacing)
        grid.point_data["Values"] = values.flatten(order="F")

        return grid

    def update_volume(self, reset_camera=False):
        """Recompute the scalar field and refresh the 3D view"""

        self.grid = self.build_grid()
        value_min = float(self.grid.point_data["Values"].min())
        value_max = float(self.grid.point_data["Values"].max())
        clim = (value_min, value_max)
        cmap = self.colormap_combo.currentText()

        if list(self.plotter.scalar_bars.keys()):
            self.plotter.remove_scalar_bar()

        if self.box_actor is not None:
            self.plotter.remove_actor(self.box_actor)
            self.box_actor = None
        if self.box_checkbox.isChecked():
            self.box_actor = self.plotter.add_mesh(
                self.grid.outline(), color="black", line_width=1, reset_camera=False)

        first_scalar_bar_shown = False

        for index, panel_widget in enumerate(self.plane_panels):
            if self.plane_actors[index] is not None:
                self.plotter.remove_actor(self.plane_actors[index])
                self.plane_actors[index] = None

            if not panel_widget.enabled:
                continue

            normal, origin = panel_widget.normal_and_origin()
            sliced = self.grid.slice(normal=normal, origin=origin)

            if sliced.n_points == 0:
                continue

            self.plane_actors[index] = self.plotter.add_mesh(
                sliced,
                scalars="Values",
                cmap=cmap,
                clim=clim,
                opacity=self.slice_opacity_slider.value(),
                show_scalar_bar=not first_scalar_bar_shown,
                scalar_bar_args={"title": "Value"},
                reset_camera=False,
            )
            first_scalar_bar_shown = True

        if self.volume_actor is not None:
            self.plotter.remove_actor(self.volume_actor)
            self.volume_actor = None

        if self.volume_checkbox.isChecked():
            try:
                self.volume_actor = self.plotter.add_volume(
                    self.grid,
                    scalars="Values",
                    cmap=cmap,
                    clim=clim,
                    opacity=[0.0, self.volume_opacity_slider.value()],
                    show_scalar_bar=False,
                    reset_camera=False,
                )
            except Exception as exc:  # pragma: no cover - depends on local GPU/driver support
                self.volume_checkbox.setChecked(False)
                QMessageBox.warning(
                    self, "Volume rendering unavailable",
                    f"Could not enable direct volume rendering on this system:\n{exc}")

        if reset_camera:
            self.plotter.reset_camera()
            self.plotter.view_isometric()

        self.status_bar.showMessage(
            f"{self.function_name}  |  grid {self.grid.dimensions[0]}^3  |  "
            f"value range [{value_min:.3f}, {value_max:.3f}]"
        )

    # --- Menu / toolbar actions -------------------------------------------

    def on_reset_camera(self):
        self.plotter.reset_camera()
        self.plotter.view_isometric()

    def on_save_screenshot(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Image (*.png)")
        if filename:
            self.plotter.screenshot(filename)
            self.status_bar.showMessage(f"Screenshot saved to {filename}", 5000)

    def on_export_volume(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Volume", "", "VTK Image Data (*.vti)")
        if filename:
            self.grid.save(filename)
            self.status_bar.showMessage(f"Volume exported to {filename}", 5000)

    def on_about(self):
        QMessageBox.information(
            self, "About",
            "Volume Explorer\n\n"
            "An interactive PyVista/Qt scalar-field slicer for the course\n"
            "\"Scientific Programming in Python and Fortran\".")

    def closeEvent(self, event):
        """Clean up the PyVista plotter before closing"""
        self.plotter.close()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = VolumeExplorerWindow()
    window.show()

    sys.exit(app.exec())
