# -*- coding: utf-8 -*-

from py5 import Sketch
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

    def draw(self):
        p5sketch.stroke(0)
        p5sketch.stroke_weight(4)
        p5sketch.point(self.x, self.y)


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

    def draw(self):
        p5sketch.stroke(0)
        p5sketch.stroke_weight(1)
        p5sketch.ellipse(self.x, self.y, self.r, self.r)


class Line:
    def __init__(self, x0=0.0, y0=0.0, x1=1.0, y1=1.0):
        self.__p0 = Point()
        self.__p1 = Point()

        self.p0.x = x0
        self.p0.y = y0
        self.p1.x = x1
        self.p1.y = y1
        
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

    def draw(self):
        p5sketch.line(self.p0.x, self.p0.y, self.p1.x, self.p1.y)

class OopSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):
        self.shapes = []

        self.shapes.append(Point(50.0, 50.0))
        self.shapes.append(Circle(100.0, 50.0, 50.0))
        self.shapes.append(Line(50.0, 50.0, 200.0, 200.0))

    def draw(self):
        for shape in self.shapes:
            shape.draw()

if __name__ == "__main__":

    global p5sketch
    p5sketch = OopSketch()
    p5sketch.run_sketch()        
