"""
Simply supported beam with a point load P at distance a from the left support.

Properties are implemented with the property() function. Compare with
beam_model_decorators.py which uses the @property decorator.

@author: Jonas Lindemann
"""


class BeamSimplySupported:
    """Computes deflection and section forces for a simply supported beam"""

    def __init__(self):
        """BeamSimplySupported constructor"""

        # Default values

        self.__a = 1.0
        self.__b = 2.0
        self.__P = 1000.0
        self.__E = 2.1e9
        self.__I = 0.1 * 0.1**3 / 12.0

    def v(self, x: float) -> float:
        """Deflection at x"""

        a = self.a
        b = self.b
        L = self.L
        P = self.P
        E = self.E
        I = self.I

        if x < a:
            return (P*b*L/(6*E*I))*((1-b**2/L**2)*x - x**3/L**2)
        else:
            return (P*a/(6*E*I))*(-a**2+(2*L+a**2/L)*x - 3*x**2+x**3/L)

    def V(self, x: float) -> float:
        """Shear force at x"""

        a = self.a
        b = self.b
        L = self.L
        P = self.P

        if x < a:
            return P*b/L
        else:
            return -P*a/L

    def M(self, x: float) -> float:
        """Bending moment at x"""

        a = self.a
        b = self.b
        L = self.L
        P = self.P

        if x < a:
            return -P*b*x/L
        else:
            return -P*a*(L-x)/L

    def x_values(self, n: int = 30) -> list[float]:
        """Return n+1 evenly spaced positions from 0 to L"""
        return [self.L * i / n for i in range(n + 1)]

    @staticmethod
    def to_float(new_value, old_value: float) -> float:
        """Convert new_value to float, keep old_value if conversion fails"""

        try:
            return float(new_value)
        except (TypeError, ValueError):
            return old_value

    # --- Get/set methods

    def get_a(self):
        return self.__a

    def set_a(self, v):
        self.__a = self.to_float(v, self.__a)

    def get_b(self):
        return self.__b

    def set_b(self, v):
        self.__b = self.to_float(v, self.__b)

    def get_L(self):
        return self.__a + self.__b

    def get_P(self):
        return self.__P

    def set_P(self, v):
        self.__P = self.to_float(v, self.__P)

    def get_E(self):
        return self.__E

    def set_E(self, v):
        self.__E = self.to_float(v, self.__E)

    def get_I(self):
        return self.__I

    def set_I(self, v):
        self.__I = self.to_float(v, self.__I)

    # --- Properties

    a = property(get_a, set_a)
    b = property(get_b, set_b)
    L = property(get_L)
    P = property(get_P, set_P)
    E = property(get_E, set_E)
    I = property(get_I, set_I)


if __name__ == "__main__":

    # Create an instance of the model class

    beam = BeamSimplySupported()

    # Print table header and section values along the beam

    print(f"{'x (m)':>10}  {'v (m)':>10}  {'V (N)':>10}  {'M (Nm)':>10}")

    for x in beam.x_values():
        print(f"{x:10.5g}  {beam.v(x):10.5g}  {beam.V(x):10.5g}  {beam.M(x):10.5g}")
