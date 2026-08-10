# -*- coding: utf-8 -*-
"""
Parametric surface functions z = f(x, y; params) used by surface_explorer.py.

Kept free of any Qt/PyVista dependency so the functions can be tried out or
tested from a plain Python/numpy session, following the same model/UI split
used by beam_model.py and beam_ui.py.

@author: Jonas Lindemann
"""

import numpy as np


class SurfaceFunction:
    """A named z = f(x, y) function together with its adjustable parameters"""

    def __init__(self, name, func, params):
        """
        name   -- display name shown in the function selector
        func   -- callable(x, y, **params) -> z, where x, y, z are ndarrays
        params -- dict of param_name -> (minimum, maximum, default, decimals)
        """
        self.name = name
        self.func = func
        self.params = params

    def evaluate(self, x, y, values):
        """Evaluate the function on the given grid using the supplied parameter values"""
        return self.func(x, y, **values)

    def default_values(self):
        """Return a dict of param_name -> default value"""
        return {name: spec[2] for name, spec in self.params.items()}


def _ripple(x, y, amplitude=2.0, frequency=3.0, phase=0.0):
    """Damped circular ripple centred on the origin"""
    r = np.sqrt(x ** 2 + y ** 2)
    return amplitude * np.sin(frequency * r + phase) / (1.0 + r)


def _gaussian_bump(x, y, amplitude=3.0, sigma=1.5):
    """Single Gaussian bump centred on the origin"""
    return amplitude * np.exp(-(x ** 2 + y ** 2) / (2.0 * sigma ** 2))


def _saddle(x, y, amplitude=1.0, scale=4.0):
    """Hyperbolic paraboloid (saddle) surface"""
    return amplitude * (x ** 2 - y ** 2) / scale


def _sinc(x, y, amplitude=3.0, frequency=1.0):
    """Sombrero / sinc surface"""
    r = np.sqrt(x ** 2 + y ** 2) * frequency
    return amplitude * np.sinc(r / np.pi)


def _egg_carton(x, y, amplitude=1.5, frequency=1.0):
    """Egg-carton wave pattern"""
    return amplitude * np.sin(frequency * x) * np.cos(frequency * y)


def _peaks(x, y, amplitude=1.0):
    """Classic 'peaks' test surface (as used in MATLAB), rescaled to a wider domain"""
    xs = x * 0.6
    ys = y * 0.6
    z = (3 * (1 - xs) ** 2 * np.exp(-(xs ** 2) - (ys + 1) ** 2)
         - 10 * (xs / 5 - xs ** 3 - ys ** 5) * np.exp(-(xs ** 2) - ys ** 2)
         - 1 / 3 * np.exp(-(xs + 1) ** 2 - ys ** 2))
    return amplitude * z


SURFACE_FUNCTIONS = {
    "Ripple": SurfaceFunction("Ripple", _ripple, {
        "amplitude": (0.1, 5.0, 2.0, 1),
        "frequency": (0.5, 10.0, 3.0, 1),
        "phase": (0.0, 6.3, 0.0, 1),
    }),
    "Gaussian Bump": SurfaceFunction("Gaussian Bump", _gaussian_bump, {
        "amplitude": (0.1, 5.0, 3.0, 1),
        "sigma": (0.2, 5.0, 1.5, 1),
    }),
    "Saddle": SurfaceFunction("Saddle", _saddle, {
        "amplitude": (0.1, 5.0, 1.0, 1),
        "scale": (0.5, 10.0, 4.0, 1),
    }),
    "Sombrero (sinc)": SurfaceFunction("Sombrero (sinc)", _sinc, {
        "amplitude": (0.1, 5.0, 3.0, 1),
        "frequency": (0.2, 5.0, 1.0, 1),
    }),
    "Egg Carton": SurfaceFunction("Egg Carton", _egg_carton, {
        "amplitude": (0.1, 5.0, 1.5, 1),
        "frequency": (0.2, 5.0, 1.0, 1),
    }),
    "Peaks": SurfaceFunction("Peaks", _peaks, {
        "amplitude": (0.1, 5.0, 1.0, 1),
    }),
}


if __name__ == "__main__":

    # Quick console sanity check, mirroring the __main__ block in beam_model.py

    x = np.linspace(-5, 5, 5)
    y = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, y)

    for name, surface_function in SURFACE_FUNCTIONS.items():
        Z = surface_function.evaluate(X, Y, surface_function.default_values())
        print(f"{name}: Z range = [{Z.min():.3f}, {Z.max():.3f}]")
