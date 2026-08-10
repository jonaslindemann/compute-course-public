# -*- coding: utf-8 -*-
"""
Parametric volumetric scalar fields value = f(x, y, z; params), used by
volume_explorer.py.

Kept free of any Qt/PyVista dependency, following the same model/UI split
used by beam_model.py, surface_functions.py and particle_model.py.

@author: Jonas Lindemann
"""

import numpy as np


class VolumeFunction:
    """A named value = f(x, y, z) scalar field together with its adjustable parameters"""

    def __init__(self, name, func, params):
        """
        name   -- display name shown in the function selector
        func   -- callable(x, y, z, **params) -> value, where x, y, z, value are ndarrays
        params -- dict of param_name -> (minimum, maximum, default, decimals)
        """
        self.name = name
        self.func = func
        self.params = params

    def evaluate(self, x, y, z, values):
        """Evaluate the field on the given grid using the supplied parameter values"""
        return self.func(x, y, z, **values)

    def default_values(self):
        """Return a dict of param_name -> default value"""
        return {name: spec[2] for name, spec in self.params.items()}


def _gaussian_blob(x, y, z, amplitude=1.0, sigma=1.5):
    """Single Gaussian blob centred on the origin"""
    r2 = x ** 2 + y ** 2 + z ** 2
    return amplitude * np.exp(-r2 / (2.0 * sigma ** 2))


def _two_blobs(x, y, z, amplitude=1.0, sigma=1.0, separation=2.5):
    """Two Gaussian blobs offset along the x axis"""
    left = np.exp(-((x + separation / 2) ** 2 + y ** 2 + z ** 2) / (2.0 * sigma ** 2))
    right = np.exp(-((x - separation / 2) ** 2 + y ** 2 + z ** 2) / (2.0 * sigma ** 2))
    return amplitude * (left + right)


def _sinc_sphere(x, y, z, amplitude=1.0, frequency=1.0):
    """Radially symmetric sombrero / sinc field"""
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2) * frequency
    return amplitude * np.sinc(r / np.pi)


def _torus_field(x, y, z, amplitude=1.0, major_radius=2.0, minor_radius=0.8):
    """Squared distance to a torus centreline, small near the torus surface"""
    q = np.sqrt(x ** 2 + y ** 2) - major_radius
    d2 = q ** 2 + z ** 2
    return amplitude * np.exp(-d2 / (2.0 * minor_radius ** 2))


def _trig_turbulence(x, y, z, amplitude=1.0, frequency=1.0):
    """Deterministic, noise-like field built from a handful of sine/cosine terms"""
    return amplitude * (
        np.sin(frequency * x) * np.cos(frequency * y) * np.sin(frequency * z)
        + 0.5 * np.sin(2.1 * frequency * y + 1.0) * np.cos(1.7 * frequency * z)
        + 0.25 * np.cos(3.3 * frequency * x + 0.5) * np.sin(2.3 * frequency * z)
    )


VOLUME_FUNCTIONS = {
    "Gaussian Blob": VolumeFunction("Gaussian Blob", _gaussian_blob, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "sigma": (0.2, 5.0, 1.5, 1),
    }),
    "Two Blobs": VolumeFunction("Two Blobs", _two_blobs, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "sigma": (0.2, 3.0, 1.0, 1),
        "separation": (0.5, 6.0, 2.5, 1),
    }),
    "Sombrero (sinc)": VolumeFunction("Sombrero (sinc)", _sinc_sphere, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "frequency": (0.2, 5.0, 1.0, 1),
    }),
    "Torus": VolumeFunction("Torus", _torus_field, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "major_radius": (0.5, 4.0, 2.0, 1),
        "minor_radius": (0.1, 2.0, 0.8, 1),
    }),
    "Trig Turbulence": VolumeFunction("Trig Turbulence", _trig_turbulence, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "frequency": (0.2, 5.0, 1.0, 1),
    }),
}


if __name__ == "__main__":

    x = np.linspace(-5, 5, 10)
    y = np.linspace(-5, 5, 10)
    z = np.linspace(-5, 5, 10)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    for name, volume_function in VOLUME_FUNCTIONS.items():
        values = volume_function.evaluate(X, Y, Z, volume_function.default_values())
        print(f"{name}: value range = [{values.min():.3f}, {values.max():.3f}]")
