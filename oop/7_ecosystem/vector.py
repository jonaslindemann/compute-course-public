# -*- coding: utf-8 -*-

import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @classmethod
    def from_angle(cls, angle, length=1.0):
        return cls(math.cos(angle) * length, math.sin(angle) * length)

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

    @property
    def angle(self):
        return math.atan2(self.y, self.x)

    def normalized(self):
        length = abs(self)
        if length == 0.0:
            return Vector2()
        return self * (1.0 / length)
