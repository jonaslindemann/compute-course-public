# -*- coding: utf-8 -*-

from py5 import Sketch
from py5base import *
import random, math

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

class DynamicBody(DrawableBase):
    def __init__(self, world, ppm=20.0):
        self.__world = world
        self.__body = None
        self.__fixture = None
        self.__ppm = 20.0

    @property
    def world(self):
        return self.__world
    
    @world.setter
    def world(self, value):
        self.__world = value

    @property
    def body(self):
        return self.__body
    
    @property
    def fixture(self):
        return self.__fixture
    
    @property
    def ppm(self):
        return self.__ppm
    
    @ppm.setter
    def ppm(self, value):
        self.__ppm = value

    def do_draw(self):
        position = self.__body.transform * self.__fixture.pos * self.__ppm



                
class Box2DSketch(Sketch):

    PPM = 20.0  # pixels per meter
    TARGET_FPS = 60
    TIME_STEP = 1.0 / TARGET_FPS
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

    def settings(self):
        self.size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def setup(self):
        self.ellipse_mode(self.CENTER)

        # --- pybox2d world setup ---
        # Create the world
        self.world = world(gravity=(0, -10), doSleep=True)

        # And a static body to hold the ground shape
        self.ground_body = world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(50, 1)),
        )

        # Create a couple dynamic bodies
        body = world.CreateDynamicBody(position=(20, 45))
        self.circle = body.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

        body = world.CreateDynamicBody(position=(30, 45), angle=15)
        self.box = body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)



    def draw(self):
        self.background(40)


if __name__ == "__main__":

    app = SketchApp()
    app.sketch = Box2DSketch()
    app.run()        
