# -*- coding: utf-8 -*-

import random, math

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

    def area(self):
        return 0.0


class Circle(Point):
    def __init__(self, x=0.0, y=0.0, r=1.0):
        super().__init__(x, y)
        self.__r = r

    @property
    def r(self):
        return self.__r

    @r.setter        
    def r(self, r):
        self.__r = r

    def copy_from(self, c):
        super().copy_from(c)
        self.r = c.r

    def area(self):
        return math.pi*math.pow(self.__r, 2)

    def __str__(self):
        return "Circle("+str(self.x)+", "+str(self.y)+", "+str(self.__r)+")"

p = Point(1.0, 2.0)
c = Circle(2.0, 4.0, 8.0)

c.r = 10.0

p.move(1.0, 1.0)
c.move(1.0, 1.0)

print(p)
print(c)
print(c.area())
