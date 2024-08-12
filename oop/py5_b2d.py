# -*- coding: utf-8 -*-

from py5 import Sketch
from py5base import *
import random, math

import numpy as np

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

global sketch
global g_world

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

class DynamicBody(DrawableBase):
    def __init__(self, body=None, fixture=None):
        self.__body = None
        self.__fixture = None
        self.__ppm = 20.0

    @property
    def body(self):
        return self.__body
    
    @body.setter
    def body(self, value):
        self.__body = value
    
    @property
    def fixture(self):
        return self.__fixture
    
    @fixture.setter
    def fixture(self, value):
        self.__fixture = value
    

class DynamicPolygon(DynamicBody):
    def __init__(self, body, fixture):
        super().__ini__(body, fixture)

    def on_draw(self):
        vertices = [(self.body.transform * v) * PPM for v in self.fixture.vertices]
        vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in self.fixture.vertices]
        sketch.points()
        pygame.draw.polygon(screen, colors[body.type], vertices)

class DynamicCircle(DynamicBody):
    def __init__(self, body, fixture):
        super().__ini__(body, fixture)

    def on_draw(self):
        pass








                
class Box2DSketch(Sketch):


    def settings(self):
        self.size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def setup(self):
        self.ellipse_mode(self.CENTER)

        # --- pybox2d world setup ---
        # Create the world
        g_world = world(gravity=(0, -10), doSleep=True)

        # And a static body to hold the ground shape
        self.ground_body = g_world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(50, 1)),
        )

        # Create a couple dynamic bodies
        body = g_world.CreateDynamicBody(position=(20, 45))
        self.circle = body.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

        body = world.CreateDynamicBody(position=(30, 45), angle=15)
        self.box = body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)



    def draw(self):
        self.background(40)


if __name__ == "__main__":

    sketch = ParticleSketch()
    sketch.run_sketch()        
