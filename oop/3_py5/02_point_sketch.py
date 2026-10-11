# -*- coding: utf-8 -*-

from py5 import Sketch

global sketch

class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def draw(self):
        sketch.stroke(0)
        sketch.stroke_weight(4)
        sketch.point(self.x, self.y)

class OopSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):
        self.p = Point()
        self.p.x = 50.0
        self.p.y = 50.0

    def draw(self):
        self.p.draw()


if __name__ == "__main__":

    sketch = OopSketch()
    sketch.run_sketch()