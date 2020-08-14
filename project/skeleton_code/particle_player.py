#!/usr/bin/env python

from tkinter import *
from math import *
from numpy import *

class Particle(object):
    canvas = None
    scaleX = 1000.0
    scaleY = 1000.0
    def __init__(self, p, r):
        self._p = p
        self._r = r
        self.id = Particle.canvas.create_oval(-4, -4, 4, 4, fill="white")
        self.update(0)
        
    def update(self, step):
        Particle.canvas.coords(self.id,
                               int(self._p[step,0]*Particle.scaleX-self._r*Particle.scaleX),
                               int(self._p[step,1]*Particle.scaleY-self._r*Particle.scaleX),
                               int(self._p[step,0]*Particle.scaleX+self._r*Particle.scaleX),
                               int(self._p[step,1]*Particle.scaleY+self._r*Particle.scaleX)
                               )
                
class Particles:
	def __init__(self, filename=""):
		self.filename = filename
		self.steps = 0
		
	def read(self):
		stateFile = open(self.filename, 'r')
		nParticles = int(stateFile.readline())
		
		self._particleDict = {}
		self._particles = []
		self._particleRadius = []
		
		# Read particle size
		
		#print("Reading particle sizes...")
		
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
			p = asarray(self._particleDict[i])
			self._particleDict[i] = p
			self._particles.append(Particle(p,0.001))
			
	def update(self, step):
		for p in self._particles:
			p.update(step)
		

    
class ParticleSimulation:
    def __init__(self, parent):
        random.seed()
        self._parent = parent
        self._canvas = Canvas(parent, width=1000, height=1000, bg="black")
        self._canvas.pack(expand=YES, fill=BOTH)
        
        Particle.canvas = self._canvas
        
        self._particles = Particles("./build/particle.state")
        self._particles.read()
        
        parent.update() # fix geometry

        self._parent.bind("<Configure>", self.onResize)
        
    def onResize(self, event=None):
    	pass
        #self._box.width = self._canvas.winfo_height()
        #self._box.height = self._canvas.winfo_height()
        
    def run(self):
    
        step = 0
    
        try:
            while 1:
                self._particles.update(step)
                self._canvas.update_idletasks()
                self._parent.update() # process events
                step += 1
                if step == self._particles.steps:
                    step = 0
        except TclError:
            pass # to avoid errors when the window is closed
        
    
if __name__ == '__main__':
        
    root = Tk()
    particleSimulation = ParticleSimulation(root)
    particleSimulation.run()
        
