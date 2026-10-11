# -*- coding: utf-8 -*-

from py5 import Sketch
import random, math

class SketchApp:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SketchApp, cls).__new__(cls)
            cls._instance.__sketch = None

        return cls._instance
            
    @property
    def sketch(self):
        return self.__sketch
    
    @sketch.setter
    def sketch(self, value):
        self.__sketch = value
    
    def run(self):
        self.__sketch.run_sketch()