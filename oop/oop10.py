# -*- coding: utf-8 -*-

import random, math

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

class Line:
    def __init__(self):
        self.__p0 = Point()
        self.__p1 = Point()
        
    @property
    def p0(self):
        return self.__p0
    
    @p0.setter
    def p0(self, p0):
        self.__p0 = p0

    @property
    def p1(self):
        return self.__p1
    
    @p1.setter
    def p1(self, p1):
        self.__p1 = p1

    @property 
    def length(self):
        return math.sqrt(
                math.pow(self.p1.x - self.p0.x, 2) + 
                math.pow(self.p1.y - self.p0.y, 2))
        
    def __str__(self):
        return_string = "Line from: \n\t"
        return_string += str(self.__p0) + "\n"
        return_string += "To: \n\t"
        return_string += str(self.__p1) + "\n"
        return_string += "Length: \n\t"
        return_string += str(self.length)+"\n"
        return return_string
        
shapes = []

shapes.append(Point(0.0, 1.0))
shapes.append(Circle(2.0, 1.0, 3.0))
shapes.append(Line())
shapes.append(42.0)

for shape in shapes:
    print(shape)
    
print(42.0.__str__())
