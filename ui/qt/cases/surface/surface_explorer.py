#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parametric Surface Explorer

A larger example application combining several of the techniques used
throughout this folder (menus, toolbars, docked controls, sliders) with
an interactive 3D view rendered by PyVista/VTK through pyvistaqt.

Pick a function, drag the parameter sliders and watch the surface update
live in 3D. Requires the extra packages "pyvista" and "pyvistaqt".

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

import surface_functions as sf

ICON_DIR = os.path.dirname(os.path.abspath(__file__))


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


class SurfaceExplorerWindow(QMainWindow):
    """Main window for the Parametric Surface Explorer application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(1200, 800)
        self.move(50, 50)
        self.setWindowTitle("Parametric Surface Explorer")

        self.function_name = next(iter(sf.SURFACE_FUNCTIONS))
        self.param_sliders = {}
        self.mesh = None
        self.actor = None

        # Create the 3D view and the docked control panel

        # 3D view

        self.plotter = QtInteractor(self)
        self.setCentralWidget(self.plotter)

        # Docked control panel

        self.dock = QDockWidget("Controls", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        panel = QWidget()
        controls_layout = QVBoxLayout(panel)

        self.function_combo = QComboBox()
        self.function_combo.addItems(sf.SURFACE_FUNCTIONS.keys())
        self.function_combo.currentTextChanged.connect(self.on_function_changed)

        function_form = QFormLayout()
        function_form.addRow("Function", self.function_combo)
        controls_layout.addLayout(function_form)

        self.param_group = QGroupBox("Function parameters")
        self.param_layout = QVBoxLayout(self.param_group)
        controls_layout.addWidget(self.param_group)

        self.grid_group = QGroupBox("Grid")
        grid_layout = QVBoxLayout(self.grid_group)
        self.resolution_slider = LabeledSlider("Resolution", 10, 300, 80, decimals=0)
        self.extent_slider = LabeledSlider("Extent", 1.0, 15.0, 5.0, decimals=1)
        self.resolution_slider.valueChanged.connect(lambda _: self.update_surface())
        self.extent_slider.valueChanged.connect(lambda _: self.update_surface())
        grid_layout.addWidget(self.resolution_slider)
        grid_layout.addWidget(self.extent_slider)
        controls_layout.addWidget(self.grid_group)

        self.appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(self.appearance_group)

        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["viridis", "plasma", "coolwarm", "terrain", "jet", "rainbow"])
        self.colormap_combo.currentTextChanged.connect(lambda _: self.update_surface())

        self.style_combo = QComboBox()
        self.style_combo.addItems(["Surface", "Surface + edges", "Wireframe", "Points"])
        self.style_combo.currentTextChanged.connect(lambda _: self.update_surface())

        self.opacity_slider = LabeledSlider("Opacity", 0.1, 1.0, 1.0, decimals=2)
        self.opacity_slider.valueChanged.connect(lambda _: self.update_surface())

        self.smooth_checkbox = QCheckBox("Smooth shading")
        self.smooth_checkbox.setChecked(True)
        self.smooth_checkbox.stateChanged.connect(lambda _: self.update_surface())

        self.axes_checkbox = QCheckBox("Show axes / bounds")
        self.axes_checkbox.setChecked(True)
        self.axes_checkbox.stateChanged.connect(lambda _: self.update_surface())

        appearance_layout.addRow("Colormap", self.colormap_combo)
        appearance_layout.addRow("Representation", self.style_combo)
        appearance_layout.addRow(self.opacity_slider)
        appearance_layout.addRow(self.smooth_checkbox)
        appearance_layout.addRow(self.axes_checkbox)

        controls_layout.addWidget(self.appearance_group)
        controls_layout.addStretch()

        self.dock.setWidget(panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.status_bar = self.statusBar()

        # Create menu bar and toolbar actions

        self.screenshot_action = QAction(icon("icons8-save.png"), "Save Screenshot...", self)
        self.screenshot_action.setShortcut("Ctrl+S")
        self.screenshot_action.triggered.connect(self.on_save_screenshot)

        self.export_action = QAction(icon("icons8-save-as.png"), "Export Mesh...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self.on_export_mesh)

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

        self.rebuild_param_controls()
        self.update_surface(reset_camera=True)

    def rebuild_param_controls(self):
        """Rebuild the sliders for the currently selected function's parameters"""

        while self.param_layout.count():
            item = self.param_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.param_sliders = {}
        surface_function = sf.SURFACE_FUNCTIONS[self.function_name]

        for param_name, (minimum, maximum, default, decimals) in surface_function.params.items():
            slider = LabeledSlider(param_name.capitalize(), minimum, maximum, default, decimals)
            slider.valueChanged.connect(lambda _: self.update_surface())
            self.param_layout.addWidget(slider)
            self.param_sliders[param_name] = slider

    def on_function_changed(self, name):
        """Handle the function selector changing"""

        self.function_name = name
        self.rebuild_param_controls()
        self.update_surface(reset_camera=True)

    def current_param_values(self):
        """Read the current parameter values from the parameter sliders"""
        return {name: slider.value() for name, slider in self.param_sliders.items()}

    def build_grid(self):
        """Evaluate the current function on a regular grid"""

        resolution = max(2, int(self.resolution_slider.value()))
        extent = self.extent_slider.value()

        x = np.linspace(-extent, extent, resolution)
        y = np.linspace(-extent, extent, resolution)
        X, Y = np.meshgrid(x, y)

        surface_function = sf.SURFACE_FUNCTIONS[self.function_name]
        Z = surface_function.evaluate(X, Y, self.current_param_values())

        return X, Y, Z

    def update_surface(self, reset_camera=False):
        """Recompute the surface and refresh the 3D view"""

        X, Y, Z = self.build_grid()

        if self.actor is not None:
            self.plotter.remove_actor(self.actor)

        self.mesh = pv.StructuredGrid(X, Y, Z)
        self.mesh["Height"] = Z.ravel(order="F")

        style_map = {
            "Surface": ("surface", False),
            "Surface + edges": ("surface", True),
            "Wireframe": ("wireframe", False),
            "Points": ("points", False),
        }
        style, show_edges = style_map[self.style_combo.currentText()]

        self.actor = self.plotter.add_mesh(
            self.mesh,
            scalars="Height",
            cmap=self.colormap_combo.currentText(),
            style=style,
            show_edges=show_edges,
            opacity=self.opacity_slider.value(),
            smooth_shading=self.smooth_checkbox.isChecked() and style == "surface",
            reset_camera=False,
        )

        self.plotter.remove_bounds_axes()
        if self.axes_checkbox.isChecked():
            self.plotter.show_bounds(grid="back", location="outer", all_edges=True)

        if reset_camera:
            self.plotter.reset_camera()
            self.plotter.view_isometric()

        z_min, z_max = float(Z.min()), float(Z.max())
        self.status_bar.showMessage(
            f"{self.function_name}  |  grid {X.shape[0]}x{X.shape[1]}  |  "
            f"Z range [{z_min:.3f}, {z_max:.3f}]"
        )

    def on_reset_camera(self):
        """Reset the camera to an isometric view of the current surface"""
        self.plotter.reset_camera()
        self.plotter.view_isometric()

    def on_save_screenshot(self):
        """Save the current 3D view as a PNG image"""

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Image (*.png)")
        if filename:
            self.plotter.screenshot(filename)
            self.status_bar.showMessage(f"Screenshot saved to {filename}", 5000)

    def on_export_mesh(self):
        """Export the current surface mesh to a file"""

        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Mesh", "", "VTK (*.vtk);;PLY (*.ply);;STL (*.stl)")
        if filename:
            self.mesh.save(filename)
            self.status_bar.showMessage(f"Mesh exported to {filename}", 5000)

    def on_about(self):
        """Show the About dialog"""
        QMessageBox.information(
            self, "About",
            "Parametric Surface Explorer\n\n"
            "An interactive PyVista/Qt example for the course\n"
            "\"Scientific Programming in Python and Fortran\".")

    def closeEvent(self, event):
        """Clean up the PyVista plotter before closing"""
        self.plotter.close()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SurfaceExplorerWindow()
    window.show()

    sys.exit(app.exec())
