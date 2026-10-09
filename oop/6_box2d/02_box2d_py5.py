# -*- coding: utf-8 -*-

from py5 import Sketch

from Box2D.b2 import world, polygonShape

global sketch

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

def to_screen(v):
    """Convert Box2D world coordinates (meters, y up) to screen pixels (y down)."""
    return v[0] * PPM, SCREEN_HEIGHT - v[1] * PPM

class DrawableBase:
    def __init__(self):
        self.stroke_color = [0, 0, 0]
        self.fill_color = [255, 255, 255]
        self.stroke_width = 1

    def on_draw(self):
        pass

    def draw(self):
        sketch.stroke(self.stroke_color[0], self.stroke_color[1], self.stroke_color[2])
        sketch.fill(self.fill_color[0], self.fill_color[1], self.fill_color[2])
        sketch.stroke_weight(self.stroke_width)

        self.on_draw()

class PhysicsBody(DrawableBase):
    def __init__(self, body):
        super().__init__()
        self.__body = body

    @property
    def body(self):
        return self.__body

    @property
    def fixture(self):
        return self.__body.fixtures[0]

class PhysicsPolygon(PhysicsBody):
    def on_draw(self):
        vertices = [to_screen(self.body.transform * v) for v in self.fixture.shape.vertices]

        sketch.begin_shape()
        for x, y in vertices:
            sketch.vertex(x, y)
        sketch.end_shape(sketch.CLOSE)

class PhysicsCircle(PhysicsBody):
    def on_draw(self):
        shape = self.fixture.shape
        x, y = to_screen(self.body.transform * shape.pos)
        d = 2 * shape.radius * PPM
        sketch.ellipse(x, y, d, d)

class Box2DSketch(Sketch):

    def settings(self):
        self.size(SCREEN_WIDTH, SCREEN_HEIGHT)

    def setup(self):
        self.ellipse_mode(self.CENTER)

        # Create the world
        self.world = world(gravity=(0, -10), doSleep=True)

        # A static body to hold the ground shape
        ground_body = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(50, 1)),
        )

        # A couple of dynamic bodies
        circle_body = self.world.CreateDynamicBody(position=(20, 45))
        circle_body.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

        box_body = self.world.CreateDynamicBody(position=(30, 45), angle=15)
        box_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

        # Wrap the Box2D bodies in drawable objects
        self.bodies = []

        ground = PhysicsPolygon(ground_body)
        ground.fill_color = [255, 255, 255]
        self.bodies.append(ground)

        circle = PhysicsCircle(circle_body)
        circle.fill_color = [127, 127, 127]
        self.bodies.append(circle)

        box = PhysicsPolygon(box_body)
        box.fill_color = [127, 127, 127]
        self.bodies.append(box)

    def draw(self):
        self.background(40)

        # Simulate one time step
        self.world.Step(TIME_STEP, 10, 10)

        for body in self.bodies:
            body.draw()

if __name__ == "__main__":

    sketch = Box2DSketch()
    sketch.run_sketch()
