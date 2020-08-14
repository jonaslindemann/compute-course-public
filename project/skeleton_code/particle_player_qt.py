# -*- coding: utf-8 -*-
"""Particle player application in PyQt5"""

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import numpy as np

class Particle(object):
    """Particle class - Visual particle representation"""
    
    # Class shared variables
    
    scene = None
    scaleX = 1000.0
    scaleY = 1000.0
    brush = QBrush(Qt.darkGreen)
    pen = QPen(Qt.NoPen)
    
    def __init__(self, p, r):
        """Particle constructor"""
        
        # Assign particle array and radius
        
        self._p = p
        self._r = r
        
        # Create QGraphicsView object
        
        self.item = Particle.scene.addEllipse(0.0, 0.0, 10.0, 10.0, Particle.pen, Particle.brush)
        
        # Do an initial update of all graphical objects
        
        self.update(0)
        
    def update(self, step):
        """Updates graphics objects to represent step"""
        
        self.item.setRect(self._p[step,0]*Particle.scaleX-self._r*Particle.scaleX,
                          self._p[step,1]*Particle.scaleY-self._r*Particle.scaleY,
                          self._r*Particle.scaleX*2.0, 
                          self._r*Particle.scaleY*2.0)
                        
class Particles:
    """Particles class - Holds a complete set of particles"""

    def __init__(self, filename=""):
        """Class constructor"""

        self.filename = filename
        self.steps = 0
        
    def read(self):
        """Read particles from state file"""
        
        stateFile = open(self.filename, 'r')
        nParticles = int(stateFile.readline())
        
        self._particleDict = {}
        self._particles = []
        self._particleRadius = []
        
        # Read particle size
        
        print("Reading particle sizes...")
        
        for i in range(nParticles):
            self._particleRadius.append(float(stateFile.readline()))

        nParticles = int(stateFile.readline())
        line = stateFile.readline()
        
        print("Reading particle traces...")
        
        j = 0
        
        while line:
            j+=1
            for i in range(nParticles):
                pos = [float(item) for item in line.strip().split()]
                if i in self._particleDict:
                    self._particleDict[i].append(pos)
                else:
                    self._particleDict[i] = []
                    self._particleDict[i].append(pos)
                
                line = stateFile.readline()
        
            if line:
                nParticles = int(line.strip())
                line = stateFile.readline()
            
        stateFile.close()    
        
        self.steps = j    
        
        # Convert to arrays and store in dict
        
        print("Converting particle traces to arrays...")
        
        for i in range(nParticles):
            p = np.asarray(self._particleDict[i])
            self._particleDict[i] = p
            self._particles.append(Particle(p,self._particleRadius[i]))
            
    def update(self, step):
        for p in self._particles:
            p.update(step)


class MainWindow:
    """Main window class for the Flow application"""

    def __init__(self, app):
        """Class constructor"""

        # Assign our application instance as a member variable

        self.app = app

        # Load and show our user interface

        self.ui = uic.loadUi('particle_player.ui')
        self.ui.show()
        self.ui.raise_()
        
        # Create a graphics view and a scene
        
        self.scene = QGraphicsScene(self.ui)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.addRect(0.0, 0.0, 1000, 1000)
        
        # Assign scene to the Particle class
        
        Particle.scene = self.scene
        
        # Read particles from file
        
        self._particles = Particles("./build/particle.state")
        self._particles.read()
        
        # Zoom view to fit our box
        
        self.ui.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        # Initialise current step counter
        
        self.step = 0
        
        # Create a timer to handle animation
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(0)
        
        
    def onTimer(self):
        """Timer callback for animating particles"""

        self._particles.update(self.step)
        self.step += 1
        if self.step == self._particles.steps:
            self.step = 0

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow(app)
    sys.exit(app.exec_())
