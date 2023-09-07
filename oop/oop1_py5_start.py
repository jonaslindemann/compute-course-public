# -*- coding: utf-8 -*-

from py5 import Sketch

global sketch

class OopSketch(Sketch):

    def settings(self):
        self.size(600, 600)

    def setup(self):
        pass

    def draw(self):
        self.background(128)

if __name__ == "__main__":

    sketch = OopSketch()
    sketch.run_sketch()