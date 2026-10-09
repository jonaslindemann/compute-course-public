# -*- coding: utf-8 -*-
"""
Live view of the ecosystem in ecosystem.py.

Left click:  add a fox
Right click: add a rabbit
Space:       pause / continue
"""

from py5 import Sketch

from ecosystem import World, Rabbit, Fox
from vector import Vector2

DT = 0.05   # simulated seconds per frame, at 60 frames/s the simulation runs 3x real time

class Py5Canvas:
    """
    The agents draw themselves by calling circle(), square() and triangle() on
    a canvas. This class translates those calls into py5 calls. Any object with
    the same three methods would work, which is called duck typing.
    """
    def __init__(self, sketch):
        self.sketch = sketch

    def circle(self, pos, radius, color):
        self.sketch.fill(*color)
        self.sketch.circle(pos.x, pos.y, 2.0 * radius)

    def square(self, pos, size, color):
        self.sketch.fill(*color)
        self.sketch.square(pos.x, pos.y, size)

    def triangle(self, pos, size, angle, color):
        tip = pos + Vector2.from_angle(angle, size)
        left = pos + Vector2.from_angle(angle + 2.5, size * 0.8)
        right = pos + Vector2.from_angle(angle - 2.5, size * 0.8)

        self.sketch.fill(*color)
        self.sketch.triangle(tip.x, tip.y, left.x, left.y, right.x, right.y)

class EcosystemSketch(Sketch):

    def settings(self):
        self.size(800, 600)

    def setup(self):
        self.rect_mode(self.CENTER)
        self.no_stroke()

        self.world = World(self.width, self.height)
        self.world.populate()

        self.canvas = Py5Canvas(self)
        self.paused = False

    def draw(self):
        self.background(30, 40, 30)

        if not self.paused:
            self.world.step(DT)

        for agent in self.world.agents:
            agent.draw(self.canvas)

        self.fill(255)
        self.text_size(14)
        self.text("Time: " + str(round(self.world.time)) + " s", 10, 20)
        self.text("Rabbits: " + str(self.world.count(Rabbit)), 10, 40)
        self.text("Foxes: " + str(self.world.count(Fox)), 10, 60)

        if self.paused:
            self.text("PAUSED", 10, 80)

    def mouse_pressed(self):
        pos = Vector2(self.mouse_x, self.mouse_y)

        if self.mouse_button == self.LEFT:
            self.world.add(Fox(pos, 20.0))
        elif self.mouse_button == self.RIGHT:
            self.world.add(Rabbit(pos, 10.0))

    def key_pressed(self):
        if self.key == " ":
            self.paused = not self.paused

if __name__ == "__main__":

    sketch = EcosystemSketch()
    sketch.run_sketch()
