# -*- coding: utf-8 -*-

import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

a = Vector2(1.0, 2.0)
b = Vector2(3.0, 4.0)

print(a)                     # __str__
print(repr(a))               # __repr__
print([a, b])                # lists show their items with __repr__

print(a + b)                 # a.__add__(b)
print(b - a)                 # b.__sub__(a)
print(a * 2.0)               # a.__mul__(2.0)
print(2.0 * a)               # float can't multiply a Vector2, so Python tries a.__rmul__(2.0)
print(-a)                    # a.__neg__()
print(abs(b))                # b.__abs__()
print(a == Vector2(1.0, 2.0))  # a.__eq__(...)

pos = Vector2(0.0, 0.0)
vel = Vector2(1.0, 0.5)
dt = 0.5

for i in range(5):
    pos += vel * dt          # no __iadd__, so Python uses pos = pos + vel * dt
    print(pos)
