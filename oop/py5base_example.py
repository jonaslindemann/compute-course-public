# -*- coding: utf-8 -*-

import random, math

from py5 import Sketch
from py5base import *

class BoxBoundary:
    def __init__(self):
        self.__xmin = 0.0
        self.__xmax = 600.0
        self.__ymin = 0.0
        self.__ymax = 600.0

    def is_inside(self, p):
        return (p.x - p.r > self.__xmin) and (p.x + p.r < self.__xmax) and (p.y - p.r > self.__ymin) and (p.y + p.r < self.__ymin)

    def check(self, p):
        if not self.is_inside(p):
            if (p.x - p.r) < self.__xmin:
                p.vx = -p.vx
                p.x = self.__xmin + p.r
            if (p.x + p.r) > self.__xmax:
                p.vx = -p.vx
                p.x = self.__xmax - p.r
            if (p.y - p.r) < self.__ymin:
                p.vy = -p.vy
                p.y = self.__ymin + p.r
            if (p.y + p.r) > self.__ymax:
                p.vy = -p.vy
                p.y = self.__ymax - p.r


class ParticleSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):

        self.particles = []
        self.boundary = BoxBoundary()
        self.ellipse_mode(self.CENTER)

        for i in range(100):
            p = RoundParticle(self.random(0,600), self.random(0, 600), self.random(30, 70))
            p.vx = self.random(-60.0, 60.0)
            p.vy = self.random(-60.0, 60.0)
            p.fill_color = [self.random(255), self.random(255), self.random(255)]
            p.fill_alpha = self.random(50, 255)
            self.particles.append(p)

    def draw(self):
        self.background(40)

        for p in self.particles:
            p.update(1.0/60.0)
            self.boundary.check(p)
            p.draw()

if __name__ == "__main__":

    app = SketchApp()
    app.sketch = ParticleSketch()
    app.run()        
