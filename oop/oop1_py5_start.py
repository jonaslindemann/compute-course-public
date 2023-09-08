# -*- coding: utf-8 -*-

from py5 import Sketch

global sketch

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        sketch.stroke(0)
        sketch.stroke_weight(4)
        sketch.point(self.x, self.y)

class Circle(Point):
    def __init__(self):
        super().__init__()
        self.r = 30
    
    def draw(self):
        sketch.stroke(0)
        sketch.stroke_weight(4)
        sketch.ellipse(self.x, self.y, self.r, self.r)

class BoxBoundary:
    def __init__(self):
        self.xmin = 0.0
        self.xmax = 600.0
        self.ymin = 0.0
        self.ymax = 600.0

    def is_inside(self, p):
        return (p.x - p.r > self.xmin) and (p.x + p.r < self.xmax) and (p.y - p.r > self.ymin) and (p.y + p.r < self.ymin)

    def check(self, p):
        if not self.is_inside(p):
            if (p.x - p.r) < self.xmin:
                p.vx = -p.vx
                p.x = self.xmin + p.r
            if (p.x + p.r) > self.xmax:
                p.vx = -p.vx
                p.x = self.xmax - p.r
            if (p.y - p.r) < self.ymin:
                p.vy = -p.vy
                p.y = self.ymin + p.r
            if (p.y + p.r) > self.ymax:
                p.vy = -p.vy
                p.y = self.ymax - p.r


class OopSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):

        self.shapes = []

        self.ellipse_mode(self.CENTER)

        for i in range(100):
            c = Circle()
            c.x = sketch.random(600)
            c.y = sketch.random(600)
            c.r = sketch.random(20, 100)
            self.shapes.append(c)

        for i in range(100):
            p = Point()
            p.x = sketch.random(600)
            p.y = sketch.random(600)
            self.shapes.append(p)

    def draw(self):
        self.background(128)
        
        for shape in self.shapes:
            shape.draw()

if __name__ == "__main__":

    sketch = OopSketch()
    sketch.run_sketch()