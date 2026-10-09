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
    pass

class RoundParticle(Particle):
    pass

class BoxBoundary:
    pass

class ParticleSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):

        self.ellipse_mode(self.CENTER)


    def draw(self):
        self.background(40)

if __name__ == "__main__":

    sketch = ParticleSketch()
    sketch.run_sketch()        
