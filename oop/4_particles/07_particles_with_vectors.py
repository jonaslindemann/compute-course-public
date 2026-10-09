# -*- coding: utf-8 -*-

from py5 import Sketch
from vector import Vector2

class DrawableBase:
    def __init__(self):
        self.__stroke_color = [0, 0, 0]
        self.__stroke_alpha = 255
        self.__fill_color = [255, 255, 255]
        self.__fill_alpha = 255
        self.__stroke_width = 1

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
        p5sketch.stroke(self.__stroke_color[0], self.__stroke_color[1], self.__stroke_color[2], self.__stroke_alpha)
        p5sketch.fill(self.__fill_color[0], self.__fill_color[1], self.__fill_color[2], self.__fill_alpha)
        p5sketch.stroke_weight(self.__stroke_width)

        self.do_draw()


class Particle(DrawableBase):
    def __init__(self, pos):
        super().__init__()
        self.__pos = pos
        self.__vel = Vector2()

        self.stroke_width = 2

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    @property
    def vel(self):
        return self.__vel

    @vel.setter
    def vel(self, vel):
        self.__vel = vel

    def update(self, dt):
        self.pos += self.vel * dt

    def do_draw(self):
        p5sketch.point(self.pos.x, self.pos.y)

class RoundParticle(Particle):
    def __init__(self, pos, r=1.0):
        super().__init__(pos)
        self.__r = r

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, r):
        self.__r = r

    def do_draw(self):
        p5sketch.ellipse(self.pos.x, self.pos.y, self.r*2, self.r*2)

class BoxBoundary:
    def __init__(self):
        self.__xmin = 0.0
        self.__xmax = 600.0
        self.__ymin = 0.0
        self.__ymax = 600.0

    def check(self, p):
        if p.pos.x - p.r < self.__xmin:
            p.pos.x = self.__xmin + p.r
            p.vel.x = -p.vel.x
        elif p.pos.x + p.r > self.__xmax:
            p.pos.x = self.__xmax - p.r
            p.vel.x = -p.vel.x
        if p.pos.y - p.r < self.__ymin:
            p.pos.y = self.__ymin + p.r
            p.vel.y = -p.vel.y
        elif p.pos.y + p.r > self.__ymax:
            p.pos.y = self.__ymax - p.r
            p.vel.y = -p.vel.y


class ParticleSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):

        self.particles = []
        self.boundary = BoxBoundary()
        self.ellipse_mode(self.CENTER)

        for i in range(100):
            p = RoundParticle(Vector2(self.random(0, 600), self.random(0, 600)), self.random(30, 70))
            p.vel = Vector2(self.random(-60.0, 60.0), self.random(-60.0, 60.0))
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

    global p5sketch
    p5sketch = ParticleSketch()
    p5sketch.run_sketch()
