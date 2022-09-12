# -*- coding: utf-8 -*-

from py5 import Sketch
import random, math

class DrawableBase:
    def __init__(self):
        self.stroke_color = [0, 0, 0]
        self.stroke_alpha = 255
        self.fill_color = [255, 255, 255]
        self.fill_alpha = 255
        self.stroke_width = 2.0
    
    def on_draw(self):
        pass

    def draw(self):
        p5sketch.stroke(self.stroke_color[0], self.stroke_color[1], self.stroke_color[2], self.stroke_alpha)
        p5sketch.fill(self.fill_color[0], self.fill_color[1], self.fill_color[2], self.fill_alpha)
        p5sketch.stroke_weight(self.stroke_width)

        self.on_draw()

class Particle(DrawableBase):
    def __init__(self, x=0.0, y=0.0, r=1.0):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def on_draw(self):
        p5sketch.ellipse(self.x, self.y, 2*self.r, 2*self.r)

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



class ParticleSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):
        self.ellipse_mode(self.CENTER)

        self.particles = []
        self.boundary = BoxBoundary()

        for i in range(30):
            p = Particle(p5sketch.random(40,550), p5sketch.random(40,550), p5sketch.random(20,50))
            p.fill_color = [p5sketch.random(255), p5sketch.random(255), p5sketch.random(255)]
            p.vx = p5sketch.random(-100, 100)
            p.vy = p5sketch.random(-100, 100)
            self.particles.append(p)


    def draw(self):
        self.background(40)

        for p in self.particles:
            p.update(1/60)
            self.boundary.check(p)
            p.draw()


if __name__ == "__main__":

    global p5sketch
    p5sketch = ParticleSketch()
    p5sketch.run_sketch()        
