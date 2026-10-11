# -*- coding: utf-8 -*-

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def set(self, x, y):
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

    def __str__(self):
        return "Point("+str(self.__x)+", "+str(self.__y)+")"

p = Point()

p.x = 42.0
p.y = 84.0

print(p)
