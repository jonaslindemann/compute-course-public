# -*- coding: utf-8 -*-

from py5 import Sketch
import random, math

global sketch

class DrawableBase:
    def __init__(self):
        self.stroke_color = [0, 0, 0]
        self.stroke_alpha = 255
        self.fill_color = [255, 255, 255]
        self.fill_alpha = 255
        self.stroke_width = 1

    def on_draw(self):
        pass

    def draw(self):
        sketch.stroke(self.stroke_color[0], self.stroke_color[1], self.stroke_color[2], self.stroke_alpha)
        sketch.fill(self.fill_color[0], self.fill_color[1], self.fill_color[2], self.fill_alpha)
        sketch.stroke_weight(self.stroke_width)

        self.on_draw()
        

class Particle(DrawableBase):
    def __init__(self, x=0.0, y=0.0):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.
        self.stroke_color = [255, 0, 0]

        self.stroke_width = 2

    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def on_draw(self):
        sketch.point(self.x, self.y)

class RoundParticle(Particle):
    def __init__(self, x=0.0, y=0.0, r=50.0):
        super().__init__(x, y)
        self.r = r

    def on_draw(self):
        sketch.ellipse(self.x, self.y, self.r*2, self.r*2)

class SquareParticle(Particle):
    def __init__(self, x=0.0, y=0.0, w=50.0, h=50.0):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.r = w/2

    def on_draw(self):
        sketch.rect(self.x, self.y, self.w, self.h)

class BoxBoundary:
    def __init__(self):
        self.xmin = 0.0
        self.xmax = 600.0
        self.ymin = 0.0
        self.ymax = 600.0

    def check(self, p):
        if p.x - p.r < self.xmin:
            p.x = self.xmin + p.r
            p.vx = -p.vx
        elif p.x + p.r > self.xmax:
            p.x = self.xmax - p.r
            p.vx = -p.vx
        if p.y - p.r < self.ymin:
            p.y = self.ymin + p.r
            p.vy = -p.vy
        elif p.y + p.r > self.ymax:
            p.y = self.ymax - p.r
            p.vy = -p.vy

class ParticleSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):

        self.ellipse_mode(self.CENTER)

        self.particles = []

        self.boundary = BoxBoundary()

        for i in range(100):
            if self.random(1) < 0.5:
                p = SquareParticle(self.random(0,600), self.random(0, 600), self.random(30, 70), self.random(30, 70))
            else:
                p = RoundParticle(self.random(0,600), self.random(0, 600), self.random(30, 70))

            p.vx = self.random(-60.0, 60.0)
            p.vy = self.random(-60.0, 60.0)
            p.fill_color = [self.random(255), self.random(255), self.random(255)]
            p.fill_alpha = self.random(50, 255)

            self.particles.append(p)


    def draw(self):
        self.background(40)

        for p in self.particles:
            p.update(1/60)
            self.boundary.check(p)
            p.draw()

if __name__ == "__main__":

    sketch = ParticleSketch()
    sketch.run_sketch()        
