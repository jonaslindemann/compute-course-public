#!/usr/bin/env python

from particle import *
from numpy import *

nParticles = 50

coords = zeros([nParticles,2],'d', order='F')
sizes = zeros([nParticles], 'd', order='F')

print("Initialise system...")

particle_driver.init_system(nParticles)
particle_driver.get_sizes(sizes)

print("Run simulation...")

for i in range(500):
	particle_driver.collision_check()
	particle_driver.boundary_check()
	particle_driver.update()
	particle_driver.get_positions(coords)
	particle_driver.write_positions()
	
print("End simulation...")
	
particle_driver.deallocate_system()
