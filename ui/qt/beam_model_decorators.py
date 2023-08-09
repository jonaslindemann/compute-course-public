# -*- coding: utf-8 -*-
"""
Fritt upplagd balk

@author: Jonas Lindemann
"""


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

    def v(self, x):
        """Beräkna deformationen vid x"""

        a = self.__a
        b = self.__b
        L = self.__L
        P = self.__P
        E = self.__E
        I = self.__I

        if x < a:
            return (P*b*L/(6*E*I))*((1-b**2/L**2)*x - x**3/L**2)
        else:
            return (P*a/(6*E*I))*(-a**2+(2*L+a**2/L)*x - 3*x**2+x**3/L)

    def V(self, x):
        """Tvärkraften vid x"""

        a = self.__a
        b = self.__b
        L = self.__L
        P = self.__P

        if x < a:
            return P*b/L
        else:
            return -P*a/L

    def M(self, x):
        """Moment vid x"""

        a = self.__a
        b = self.__b
        L = self.__L
        P = self.__P

        if x < a:
            return -P*b*x/L
        else:
            return -P*a*(L-x)/L

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
