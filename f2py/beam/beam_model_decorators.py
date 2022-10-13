# -*- coding: utf-8 -*-
"""
Fritt upplagd balk

@author: Jonas Lindemann
"""

import os

os.add_dll_directory(os.path.join(os.getcwd(), "./beam/.libs"))

from beam import *

class BeamSimplySupported:
    """Klass för att beräkna fritt upplagd balk"""
    def __init__(self):
        """BeamSimplySupported konstruktor"""

        # Initiera standardvärden

        self.__a = 1.0
        self.__b = 2.0
        self.__L = self.a + self.b
        self.__P = 1000
        self.__E = 2.1e9
        self.__I = 0.1*0.1**4/12.0

        self.update_params()

    def update_params(self):
        beam_model.a = self.__a
        beam_model.b = self.__b
        beam_model.P = self.__P
        beam_model.E = self.__E
        beam_model.I = self.__I
        beam_model.L = self.__a + self.__b

    def v(self, x):
        """Beräkna deformationen vid x"""

        self.update_params()
        return beam_model.deflections(x)   

    def V(self, x):
        """Tvärkraften vid x"""

        self.update_params()
        return beam_model.shear_forces(x)   

    def M(self, x):
        """Moment vid x"""

        self.update_params()
        return beam_model.moments(x)

    def to_float(self, new_value, old_value):
        """Hantera tilldelning av egenskaper på ett säkert sätt"""

        try:
            v = float(new_value)
        except ValueError:
            return old_value

        return v

    # --- Get/Set metoder

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, v):
        self.__a = self.to_float(v, self.__a)

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, v):
        self.__b = self.to_float(v, self.__b)

    @property
    def P(self):
        return self.__P

    @P.setter
    def P(self, v):
        self.__P = self.to_float(v, self.__P)

    @property
    def L(self):
        return self.__a + self.__b

    @property
    def E(self):
        return self.__E

    @E.setter
    def E(self, v):
        self.__E = self.to_float(v, self.__E)

    @property
    def I(self):
        return self.__I

    @I.setter
    def I(self, v):
        self.__I = self.to_float(v, self.__I)

    # Egenskaper

if __name__ == "__main__":

    # Skapa en instans av modellklassen

    beam = BeamSimplySupported()

    # Initiera loopvariabler

    x = 0.0
    dx = 0.1

    # Skriv ut tabellhuvud

    print('{:>10}  {:>10}  {:>10}  {:>10}'.format("x (m)", "v (m)", "V (N)", "M (Nm)"))

    # Loopa över x och skriv ut snittkrafter

    while x < beam.L + dx:
        print('{:10.5}, {:10.5}, {:10.5}, {:10.5}'.format(x, beam.v(x), beam.V(x), beam.M(x)))
        x += dx
