# -*- coding: utf-8 -*-
"""
Interactive bridge. The structure is solved again every frame.

Mouse:       move the load along the deck
Up/Down:     increase / decrease the load
S:           switch between stiff and soft bearings
+/-:         change the displacement scale
"""

import math

from py5 import Sketch

from structure import Spring
from bridge import create_bridge, set_bearing_stiffness

PPM = 70.0          # pixels per meter
MARGIN = 80.0       # pixels left of the bridge
BASE_Y = 300.0      # screen y of the deck (y = 0)
FORCE_REF = 300e3   # N, force drawn with full colour

STIFF_BEARINGS = 5e7
SOFT_BEARINGS = 1e7

class BridgeSketch(Sketch):

    def settings(self):
        self.size(1000, 500)

    def setup(self):
        self.bridge, self.deck = create_bridge(bearing_stiffness=STIFF_BEARINGS)
        self.load = 100e3
        self.scale = 50.0
        self.soft_bearings = False

        self.gray = self.color(190)
        self.red = self.color(220, 50, 40)
        self.blue = self.color(40, 80, 220)

    def to_screen(self, x, y):
        return MARGIN + x * PPM, BASE_Y - y * PPM

    def deformed(self, node):
        return self.to_screen(node.x + self.scale * node.ux, node.y + self.scale * node.uy)

    def nearest_deck_node(self, mouse_x):
        x = (mouse_x - MARGIN) / PPM
        return min(self.deck, key=lambda node: abs(node.x - x))

    def draw(self):
        load_node = self.nearest_deck_node(self.mouse_x)

        self.bridge.clear_loads()
        self.bridge.add_load(load_node, 0.0, -self.load)
        self.bridge.solve()

        self.background(250)
        self.draw_ground()
        self.draw_undeformed()

        for element in self.bridge.elements:
            if isinstance(element, Spring):
                self.draw_spring(element)
            else:
                self.draw_bar(element)

        self.draw_load(load_node)
        self.draw_info()

    def draw_ground(self):
        x0, y0 = self.to_screen(-1.0, -1.0)
        x1, y1 = self.to_screen(13.0, -1.0)

        self.no_stroke()
        self.fill(225)
        self.rect(x0, y0, x1 - x0, self.height - y0)

    def draw_undeformed(self):
        self.stroke(215)
        self.stroke_weight(1)

        for element in self.bridge.elements:
            x0, y0 = self.to_screen(element.node0.x, element.node0.y)
            x1, y1 = self.to_screen(element.node1.x, element.node1.y)
            self.line(x0, y0, x1, y1)

    def draw_bar(self, bar):
        amount = min(abs(bar.force) / FORCE_REF, 1.0)

        if bar.force > 0.0:
            self.stroke(self.lerp_color(self.gray, self.red, amount))
        else:
            self.stroke(self.lerp_color(self.gray, self.blue, amount))

        self.stroke_weight(2.0 + 5.0 * amount)

        x0, y0 = self.deformed(bar.node0)
        x1, y1 = self.deformed(bar.node1)
        self.line(x0, y0, x1, y1)

    def draw_spring(self, spring, n_zigs=6, width=7.0):
        x0, y0 = self.deformed(spring.node0)
        x1, y1 = self.deformed(spring.node1)

        length = math.hypot(x1 - x0, y1 - y0)
        nx, ny = -(y1 - y0) / length, (x1 - x0) / length    # normal to the spring

        self.stroke(40, 150, 60)
        self.stroke_weight(2)
        self.no_fill()

        self.begin_shape()
        self.vertex(x0, y0)
        for i in range(1, 2 * n_zigs):
            t = i / (2 * n_zigs)
            side = width if i % 2 == 1 else -width
            self.vertex(x0 + t * (x1 - x0) + side * nx, y0 + t * (y1 - y0) + side * ny)
        self.vertex(x1, y1)
        self.end_shape()

    def draw_load(self, node):
        x, y = self.deformed(node)
        arrow_length = 30.0 + 80.0 * self.load / FORCE_REF

        self.stroke(0)
        self.stroke_weight(3)
        self.line(x, y - arrow_length, x, y - 8)

        self.no_stroke()
        self.fill(0)
        self.triangle(x, y, x - 6, y - 12, x + 6, y - 12)

        self.text_align(self.CENTER)
        self.text(str(round(self.load / 1e3)) + " kN", x, y - arrow_length - 8)
        self.text_align(self.LEFT)

    def draw_info(self):
        bars = [element for element in self.bridge.elements if not isinstance(element, Spring)]
        max_tension = max(bar.force for bar in bars)
        max_compression = min(bar.force for bar in bars)

        if self.soft_bearings:
            bearings = "soft"
        else:
            bearings = "stiff"

        self.fill(30)
        self.text_size(14)
        self.text("Max displacement: " + str(round(self.bridge.max_displacement() * 1e3, 1)) + " mm"
                  + "    Max tension: " + str(round(max_tension / 1e3)) + " kN"
                  + "    Max compression: " + str(round(-max_compression / 1e3)) + " kN"
                  + "    Bearings: " + bearings
                  + "    Displacements scaled " + str(round(self.scale)) + "x", 20, 30)

        self.fill(110)
        self.text("Move the mouse to move the load.  Up/Down: load.  S: bearings.  +/-: scale.", 20, self.height - 20)

    def key_pressed(self):
        if self.key == self.CODED:
            if self.key_code == self.UP:
                self.load = min(self.load + 25e3, FORCE_REF)
            elif self.key_code == self.DOWN:
                self.load = max(self.load - 25e3, 0.0)
        elif self.key in ("s", "S"):
            self.soft_bearings = not self.soft_bearings
            if self.soft_bearings:
                set_bearing_stiffness(self.bridge, SOFT_BEARINGS)
            else:
                set_bearing_stiffness(self.bridge, STIFF_BEARINGS)
        elif self.key == "+":
            self.scale *= 1.5
        elif self.key == "-":
            self.scale /= 1.5

if __name__ == "__main__":

    sketch = BridgeSketch()
    sketch.run_sketch()
