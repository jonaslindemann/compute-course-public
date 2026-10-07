"""
Simply supported beam with a point load P at distance a from the left support.

Properties are implemented with the @property decorator. Compare with
beam_model.py which uses the property() function.

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

    # --- Properties

    @property
    def a(self) -> float:
        return self.__a

    @a.setter
    def a(self, v) -> None:
        self.__a = self.to_float(v, self.__a)

    @property
    def b(self) -> float:
        return self.__b

    @b.setter
    def b(self, v) -> None:
        self.__b = self.to_float(v, self.__b)

    @property
    def L(self) -> float:
        """Beam length. Always computed from a and b."""
        return self.__a + self.__b

    @property
    def P(self) -> float:
        return self.__P

    @P.setter
    def P(self, v) -> None:
        self.__P = self.to_float(v, self.__P)

    @property
    def E(self) -> float:
        return self.__E

    @E.setter
    def E(self, v) -> None:
        self.__E = self.to_float(v, self.__E)

    @property
    def I(self) -> float:
        return self.__I

    @I.setter
    def I(self, v) -> None:
        self.__I = self.to_float(v, self.__I)


if __name__ == "__main__":

    # Create an instance of the model class

    beam = BeamSimplySupported()

    # Print table header and section values along the beam

    print(f"{'x (m)':>10}  {'v (m)':>10}  {'V (N)':>10}  {'M (Nm)':>10}")

    for x in beam.x_values():
        print(f"{x:10.5g}  {beam.v(x):10.5g}  {beam.V(x):10.5g}  {beam.M(x):10.5g}")
