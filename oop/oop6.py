# -*- coding: utf-8 -*-

import random

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def set(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return "Point("+str(self._x)+", "+str(self._y)+")"

p0 = Point(0.0, 0.0)
p1 = Point(1.0, 2.0)

p2 = p0
p3 = p1

print(id(p0))
print(id(p1))
print(id(p2))
print(id(p3))