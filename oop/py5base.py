# -*- coding: utf-8 -*-

from py5 import Sketch
import random, math

class SketchApp:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SketchApp, cls).__new__(cls)
            cls._instance.__sketch = None

        return cls._instance
            
    @property
    def sketch(self):
        return self.__sketch
    
    @sketch.setter
    def sketch(self, value):
        self.__sketch = value
    
    def run(self):
        self.__sketch.run_sketch()

class DrawableBase:
    def __init__(self):
        self.__sketch = SketchApp().sketch
        self.__stroke_color = [0, 0, 0]
        self.__stroke_alpha = 255
        self.__fill_color = [255, 255, 255]
        self.__fill_alpha = 255
        self.__stroke_width = 1

    @property
    def sketch(self):
        return self.__sketch

    @property
    def stroke_color(self):
        return self.__stroke_color

    @stroke_color.setter
    def stroke_color(self, color):
        self.__stroke_color = color

    @property
    def stroke_alpha(self):
        return self.__stroke_alpha

    @stroke_alpha.setter
    def stroke_alpha(self, v):
        self.__stroke_alpha = v

    @property
    def fill_color(self):
        return self.__fill_color
        
    @fill_color.setter
    def fill_color(self, color):
        self.__fill_color = color

    @property
    def fill_alpha(self):
        return self.__fill_alpha

    @fill_alpha.setter
    def fill_alpha(self, v):
        self.__fill_alpha = v

    @property
    def stroke_width(self):
        return self.__stroke_width

    @stroke_width.setter
    def stroke_width(self, width):
        self.__stroke_width = width

    def do_draw(self):
        pass

    def draw(self):
        self.sketch.stroke(self.__stroke_color[0], self.__stroke_color[1], self.__stroke_color[2], self.__stroke_alpha)
        self.sketch.fill(self.__fill_color[0], self.__fill_color[1], self.__fill_color[2], self.__fill_alpha)
        self.sketch.stroke_weight(self.__stroke_width)

        self.do_draw()
        

class Particle(DrawableBase):
    def __init__(self, x=0.0, y=0.0):
        super().__init__()
        self.__x = x
        self.__y = y
        self.__vx = 0.0
        self.__vy = 0.0

        self.stroke_width = 2

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

    @property
    def vx(self):
        return self.__vx

    @vx.setter
    def vx(self, v):
        self.__vx = v

    @property
    def vy(self):
        return self.__vy

    @vy.setter
    def vy(self, v):
        self.__vy = v

    def update(self, dt):
        self.__x += self.__vx*dt
        self.__y += self.__vy*dt

    def do_draw(self):
        self.sketch.point(self.x, self.y)

class RoundParticle(Particle):
    def __init__(self, x=0.0, y=0.0, r=1.0):
        super().__init__(x, y)
        self.__r = r

    @property
    def r(self):
        return self.__r

    @r.setter        
    def r(self, r):
        self.__r = r

    def do_draw(self):
        self.sketch.ellipse(self.x, self.y, self.r*2, self.r*2)

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
