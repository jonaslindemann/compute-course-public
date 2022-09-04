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
        self.__x = x
        self.__y = y

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

    def copy_from(self, p):
        self.__x = p.x
        self.__y = p.y

    def __str__(self):
        return "Point("+str(self.__x)+", "+str(self.__y)+")"

p0 = Point()
p1 = Point()

p0.move(10.0, 20.0)
p0.move(-5.0, -5.0)

print(p0.x, p0.y)

p1.copy_from(p0)
print(p1.x, p0.y)

