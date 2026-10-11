#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D Particle Explorer

A companion to surface_explorer.py: an interactive PyVista/Qt application
that animates a 3D "particles in a box" simulation (see particle_model.py
and project/particles_in_a_box.md for the original 2D exercise this is
based on).

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
    QLabel, QPushButton, QAction, QFileDialog, QMessageBox, QStyle,
)
from qtpy.QtCore import Qt, Signal, QTimer
from qtpy.QtGui import QIcon

import particle_model as pm

ICON_DIR = os.path.dirname(os.path.abspath(__file__))

DT = 1.0 / 60.0  # fixed simulation timestep (s)


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


class ParticleExplorerWindow(QMainWindow):
    """Main window for the 3D Particle Explorer application"""

    def __init__(self):
        """Class constructor"""
        super().__init__()

        self.resize(1200, 800)
        self.move(50, 50)
        self.setWindowTitle("3D Particle Explorer")

        self.system = pm.ParticleSystem(n_particles=150, box_size=1.0, radius=0.02, speed=0.6)
        self.point_cloud = None
        self.particle_actor = None
        self.box_actor = None
        self.playing = True
        self.elapsed_time = 0.0

        # Create the 3D view and the docked control panel

        # 3D view

        self.plotter = QtInteractor(self)
        self.setCentralWidget(self.plotter)

        # Docked control panel

        self.dock = QDockWidget("Controls", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        panel = QWidget()
        controls_layout = QVBoxLayout(panel)

        # Playback

        playback_group = QGroupBox("Playback")
        playback_layout = QHBoxLayout(playback_group)

        style = self.style()

        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(style.standardIcon(QStyle.SP_MediaPause))
        self.play_pause_button.setText("Pause")
        self.play_pause_button.clicked.connect(self.on_toggle_play)

        self.step_button = QPushButton()
        self.step_button.setIcon(style.standardIcon(QStyle.SP_MediaSkipForward))
        self.step_button.setText("Step")
        self.step_button.clicked.connect(self.on_step)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(style.standardIcon(QStyle.SP_BrowserReload))
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.on_reset)

        playback_layout.addWidget(self.play_pause_button)
        playback_layout.addWidget(self.step_button)
        playback_layout.addWidget(self.reset_button)
        controls_layout.addWidget(playback_group)

        # Initial conditions (applied on Reset)

        init_group = QGroupBox("Initial conditions (Reset to apply)")
        init_layout = QVBoxLayout(init_group)

        self.num_particles_slider = LabeledSlider("Particles", 10, 400, 150, decimals=0)
        self.box_size_slider = LabeledSlider("Box size", 0.2, 3.0, 1.0, decimals=1)
        self.radius_slider = LabeledSlider("Radius", 0.005, 0.05, 0.02, decimals=3)
        self.speed_slider = LabeledSlider("Speed", 0.1, 3.0, 0.6, decimals=2)

        init_layout.addWidget(self.num_particles_slider)
        init_layout.addWidget(self.box_size_slider)
        init_layout.addWidget(self.radius_slider)
        init_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(init_group)

        # Physics (applied live)

        physics_group = QGroupBox("Physics")
        physics_layout = QVBoxLayout(physics_group)

        self.gravity_slider = LabeledSlider("Gravity", 0.0, 5.0, 0.0, decimals=2)
        self.gravity_slider.valueChanged.connect(self.on_gravity_changed)

        self.restitution_slider = LabeledSlider("Restitution", 0.1, 1.0, 1.0, decimals=2)
        self.restitution_slider.valueChanged.connect(self.on_restitution_changed)

        self.time_scale_slider = LabeledSlider("Time scale", 0.1, 3.0, 1.0, decimals=2)

        self.collisions_checkbox = QCheckBox("Particle-particle collisions (O(n^2))")
        self.collisions_checkbox.stateChanged.connect(self.on_collisions_changed)

        physics_layout.addWidget(self.gravity_slider)
        physics_layout.addWidget(self.restitution_slider)
        physics_layout.addWidget(self.time_scale_slider)
        physics_layout.addWidget(self.collisions_checkbox)
        controls_layout.addWidget(physics_group)

        # Appearance

        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(appearance_group)

        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["viridis", "plasma", "coolwarm", "turbo", "jet", "rainbow"])
        self.colormap_combo.currentTextChanged.connect(self.on_colormap_changed)

        self.point_size_slider = LabeledSlider("Point size", 2.0, 30.0, 10.0, decimals=0)
        self.point_size_slider.valueChanged.connect(self.on_point_size_changed)

        self.box_checkbox = QCheckBox("Show box")
        self.box_checkbox.setChecked(True)
        self.box_checkbox.stateChanged.connect(self.on_box_visibility_changed)

        appearance_layout.addRow("Colormap", self.colormap_combo)
        appearance_layout.addRow(self.point_size_slider)
        appearance_layout.addRow(self.box_checkbox)

        controls_layout.addWidget(appearance_group)
        controls_layout.addStretch()

        self.dock.setWidget(panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.status_bar = self.statusBar()

        # Create menu bar and toolbar actions

        self.screenshot_action = QAction(icon("icons8-save.png"), "Save Screenshot...", self)
        self.screenshot_action.setShortcut("Ctrl+S")
        self.screenshot_action.triggered.connect(self.on_save_screenshot)

        self.export_action = QAction(icon("icons8-save-as.png"), "Export Particles...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self.on_export_particles)

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

        sim_menu = self.menuBar().addMenu("&Simulation")
        sim_menu.addAction(self.play_pause_action())
        sim_menu.addAction(self.step_action())
        sim_menu.addAction(self.reset_action())

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

        self.rebuild_scene(reset_camera=True)

        self.timer = QTimer(self)
        self.timer.setInterval(int(DT * 1000))
        self.timer.timeout.connect(self.on_timer)
        self.timer.start()

    def play_pause_action(self):
        action = QAction("Play/Pause", self)
        action.setShortcut("Space")
        action.triggered.connect(self.on_toggle_play)
        return action

    def step_action(self):
        action = QAction("Step", self)
        action.triggered.connect(self.on_step)
        return action

    def reset_action(self):
        action = QAction("Reset", self)
        action.triggered.connect(self.on_reset)
        return action

    # --- Scene construction ---------------------------------------------

    def rebuild_scene(self, reset_camera=False):
        """(Re)build the box outline and the particle point cloud actors"""

        if self.particle_actor is not None:
            self.plotter.remove_actor(self.particle_actor)
        if self.box_actor is not None:
            self.plotter.remove_actor(self.box_actor)
            self.box_actor = None

        self.point_cloud = pv.PolyData(self.system.positions)
        self.point_cloud["Speed"] = self.system.speeds

        self.particle_actor = self.plotter.add_mesh(
            self.point_cloud,
            scalars="Speed",
            cmap=self.colormap_combo.currentText(),
            render_points_as_spheres=True,
            point_size=self.point_size_slider.value(),
            reset_camera=False,
        )

        if self.box_checkbox.isChecked():
            box = pv.Box(bounds=(0.0, self.system.box_size,
                                  0.0, self.system.box_size,
                                  0.0, self.system.box_size))
            self.box_actor = self.plotter.add_mesh(
                box, style="wireframe", color="black", line_width=1, reset_camera=False)

        if reset_camera:
            self.plotter.reset_camera()
            self.plotter.view_isometric()

        self.update_status_bar()

    def update_status_bar(self):
        self.status_bar.showMessage(
            f"{self.system.n_particles} particles  |  box {self.system.box_size:.2f}  |  "
            f"t = {self.elapsed_time:6.2f} s  |  mean speed = {self.system.speeds.mean():.3f}"
        )

    # --- Simulation loop ---------------------------------------------------

    def on_timer(self):
        if self.playing:
            self.advance_simulation()

    def advance_simulation(self):
        dt = DT * self.time_scale_slider.value()
        self.system.step(dt)
        self.elapsed_time += dt

        self.point_cloud.points = self.system.positions
        self.point_cloud["Speed"] = self.system.speeds
        self.plotter.render()

        self.update_status_bar()

    def on_toggle_play(self):
        self.playing = not self.playing
        if self.playing:
            self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_pause_button.setText("Pause")
        else:
            self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_pause_button.setText("Play")

    def on_step(self):
        self.playing = False
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_pause_button.setText("Play")
        self.advance_simulation()

    def on_reset(self):
        self.system.box_size = self.box_size_slider.value()
        self.system.radius = self.radius_slider.value()
        self.system.reset(
            n_particles=int(self.num_particles_slider.value()),
            speed=self.speed_slider.value())
        self.elapsed_time = 0.0
        self.rebuild_scene(reset_camera=True)

    # --- Live parameter handlers -----------------------------------------

    def on_gravity_changed(self, value):
        self.system.gravity = value

    def on_restitution_changed(self, value):
        self.system.restitution = value

    def on_collisions_changed(self, _state):
        self.system.collisions_enabled = self.collisions_checkbox.isChecked()

    def on_colormap_changed(self, name):
        self.particle_actor.mapper.lookup_table = pv.LookupTable(cmap=name)
        self.plotter.render()

    def on_point_size_changed(self, value):
        self.particle_actor.prop.point_size = value
        self.plotter.render()

    def on_box_visibility_changed(self, _state):
        if self.box_actor is not None:
            self.plotter.remove_actor(self.box_actor)
            self.box_actor = None
        if self.box_checkbox.isChecked():
            box = pv.Box(bounds=(0.0, self.system.box_size,
                                  0.0, self.system.box_size,
                                  0.0, self.system.box_size))
            self.box_actor = self.plotter.add_mesh(
                box, style="wireframe", color="black", line_width=1, reset_camera=False)
        self.plotter.render()

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

    def on_export_particles(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Particles", "", "VTK (*.vtk);;PLY (*.ply)")
        if filename:
            self.point_cloud.save(filename)
            self.status_bar.showMessage(f"Particles exported to {filename}", 5000)

    def on_about(self):
        QMessageBox.information(
            self, "About",
            "3D Particle Explorer\n\n"
            "An interactive PyVista/Qt particles-in-a-box simulation for the course\n"
            "\"Scientific Programming in Python and Fortran\".")

    def closeEvent(self, event):
        """Clean up the timer and the PyVista plotter before closing"""
        self.timer.stop()
        self.plotter.close()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ParticleExplorerWindow()
    window.show()

    sys.exit(app.exec())
