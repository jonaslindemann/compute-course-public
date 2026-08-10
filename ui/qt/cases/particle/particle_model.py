# -*- coding: utf-8 -*-
"""
3D particle-in-a-box simulation model used by particle_explorer.py.

Kept free of any Qt/PyVista dependency, following the same model/UI split
used by beam_model.py and surface_functions.py. This is a 3D, vectorised
take on the "particles in a box" exercise from project/particles_in_a_box.md:
equal-mass particles move in straight lines inside a cubic box, bounce off
the walls, and can optionally exchange momentum in elastic collisions with
each other and fall under gravity.

@author: Jonas Lindemann
"""

import numpy as np


class ParticleSystem:
    """A system of equal-mass, equal-radius particles bouncing inside a cubic box"""

    def __init__(self, n_particles=150, box_size=1.0, radius=0.02, speed=0.6):
        """Class constructor"""

        self.box_size = box_size
        self.radius = radius
        self.speed = speed

        self.gravity = 0.0
        self.restitution = 1.0
        self.collisions_enabled = False

        self.n_particles = n_particles
        self.positions = None
        self.velocities = None

        self.reset(n_particles, speed)

    def reset(self, n_particles=None, speed=None):
        """Re-seed the system with new random positions and velocities"""

        if n_particles is not None:
            self.n_particles = n_particles
        if speed is not None:
            self.speed = speed

        margin = self.radius
        low, high = margin, self.box_size - margin

        rng = np.random.default_rng()
        self.positions = rng.uniform(low, high, size=(self.n_particles, 3))

        # Random directions on the unit sphere, scaled to the chosen speed

        directions = rng.normal(size=(self.n_particles, 3))
        norms = np.linalg.norm(directions, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        self.velocities = directions / norms * self.speed

    def step(self, dt):
        """Advance the simulation by dt seconds"""

        if self.gravity:
            self.velocities[:, 2] -= self.gravity * dt

        self.positions += self.velocities * dt

        self._resolve_wall_collisions()

        if self.collisions_enabled and self.n_particles > 1:
            self._resolve_particle_collisions()

    def _resolve_wall_collisions(self):
        """Bounce particles off the six walls of the box"""

        r = self.radius
        low = r
        high = self.box_size - r

        for axis in range(3):
            below = self.positions[:, axis] < low
            self.positions[below, axis] = low
            self.velocities[below, axis] *= -self.restitution

            above = self.positions[:, axis] > high
            self.positions[above, axis] = high
            self.velocities[above, axis] *= -self.restitution

    def _resolve_particle_collisions(self):
        """Resolve pairwise elastic collisions between particles (O(n^2))

        As in the original exercise, a particle colliding with more than one
        other particle in the same step is not modelled exactly -- each
        colliding pair is simply resolved in turn.
        """

        min_dist_sq = (2.0 * self.radius) ** 2

        for i in range(self.n_particles - 1):
            diff = self.positions[i + 1:] - self.positions[i]
            dist_sq = np.einsum("ij,ij->i", diff, diff)
            colliding = np.nonzero((dist_sq > 0.0) & (dist_sq < min_dist_sq))[0]

            for k in colliding:
                self._collide_pair(i, i + 1 + k)

    def _collide_pair(self, i, j):
        """Elastic collision between two equal-mass particles i and j"""

        delta_pos = self.positions[i] - self.positions[j]
        dist_sq = np.dot(delta_pos, delta_pos)
        if dist_sq == 0.0:
            return

        delta_vel = self.velocities[i] - self.velocities[j]
        factor = np.dot(delta_vel, delta_pos) / dist_sq

        self.velocities[i] -= factor * delta_pos
        self.velocities[j] += factor * delta_pos

        # Push the pair apart so they do not keep re-triggering the collision

        dist = np.sqrt(dist_sq)
        overlap = 2.0 * self.radius - dist
        if overlap > 0.0:
            correction = (delta_pos / dist) * (overlap / 2.0)
            self.positions[i] += correction
            self.positions[j] -= correction

    @property
    def speeds(self):
        """Per-particle speed magnitude, used for colouring the particles"""
        return np.linalg.norm(self.velocities, axis=1)


if __name__ == "__main__":

    system = ParticleSystem(n_particles=20)
    system.collisions_enabled = True
    system.gravity = 1.0

    for step in range(5):
        system.step(0.05)
        print(f"step {step}: mean speed = {system.speeds.mean():.4f}, "
              f"max speed = {system.speeds.max():.4f}")
