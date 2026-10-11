# -*- coding: utf-8 -*-
"""
A small predator-prey ecosystem: grass, rabbits and foxes.

This module contains only the simulation. It doesn't import any graphics
library, so the same classes can be plotted with matplotlib
(01_population_plot.py) or animated with py5 (02_ecosystem_py5.py).
"""

import math, random

from vector import Vector2

class Agent:
    """Base class for everything that lives in the world."""

    # Class attributes: shared by all agents of a class, overridden in subclasses.
    color = (255, 255, 255)
    radius = 4.0
    speed = 0.0
    vision = 0.0
    metabolism = 0.0        # energy used per second
    birth_energy = None     # energy needed to reproduce, None = never reproduces

    def __init__(self, pos, energy=10.0):
        self.pos = pos
        self.vel = Vector2()
        self.heading = random.uniform(0.0, 2.0 * math.pi)
        self.energy = energy
        self.alive = True

    def update(self, world, dt):
        self.behave(world, dt)
        self.move(world, dt)

        self.energy -= self.metabolism * dt

        if self.energy <= 0.0:
            self.die()
        elif self.birth_energy is not None and self.energy > self.birth_energy:
            self.reproduce(world)

    def behave(self, world, dt):
        """Decide where to go. Overridden by the animals."""
        pass

    def move(self, world, dt):
        self.pos += self.vel * dt
        world.keep_inside(self)

    def wander(self, dt):
        self.heading += random.uniform(-3.0, 3.0) * dt
        self.vel = Vector2.from_angle(self.heading, self.speed)

    def move_towards(self, target):
        self.vel = (target.pos - self.pos).normalized() * self.speed
        self.heading = self.vel.angle

    def move_away_from(self, target):
        self.move_towards(target)
        self.vel = -self.vel
        self.heading = self.vel.angle

    def touches(self, other):
        return abs(other.pos - self.pos) < self.radius + other.radius

    def reproduce(self, world):
        self.energy /= 2.0

        # type(self) is the class of this object, so rabbits create
        # rabbits and foxes create foxes, without overriding this method.

        offset = Vector2(random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0))
        world.add(type(self)(self.pos + offset, self.energy))

    def die(self):
        self.alive = False

    def draw(self, canvas):
        canvas.circle(self.pos, self.radius, self.color)


class Grass(Agent):
    color = (60, 170, 60)
    eaten_color = (45, 65, 40)
    radius = 3.0
    regrow_time = 10.0

    def __init__(self, pos, energy=0.0):
        super().__init__(pos, energy)
        self.regrow_timer = 0.0

    @property
    def grown(self):
        return self.regrow_timer <= 0.0

    def update(self, world, dt):
        # Grass doesn't move, use energy or reproduce. It only regrows.
        if self.regrow_timer > 0.0:
            self.regrow_timer -= dt

    def eaten(self):
        self.regrow_timer = self.regrow_time

    def draw(self, canvas):
        if self.grown:
            canvas.square(self.pos, 2.0 * self.radius, self.color)
        else:
            canvas.square(self.pos, 2.0 * self.radius, self.eaten_color)


class Rabbit(Agent):
    color = (235, 235, 235)
    radius = 4.0
    speed = 40.0
    vision = 50.0
    metabolism = 1.0
    birth_energy = 20.0
    food_energy = 4.0

    def behave(self, world, dt):
        fox = world.nearest(self.pos, Fox, self.vision)

        if fox is not None:
            self.move_away_from(fox)
            return

        grass = world.nearest(self.pos, Grass, self.vision, lambda g: g.grown)

        if grass is None:
            self.wander(dt)
        elif self.touches(grass):
            grass.eaten()
            self.energy += self.food_energy
        else:
            self.move_towards(grass)


class Fox(Agent):
    color = (235, 120, 40)
    radius = 6.0
    speed = 43.0
    vision = 70.0
    metabolism = 0.7
    birth_energy = 30.0
    food_energy = 15.0
    hungry_energy = 25.0    # foxes only hunt when their energy is below this

    @property
    def hungry(self):
        return self.energy < self.hungry_energy

    def behave(self, world, dt):
        rabbit = None

        if self.hungry:
            rabbit = world.nearest(self.pos, Rabbit, self.vision)

        if rabbit is None:
            self.wander(dt)
        elif self.touches(rabbit):
            rabbit.die()
            self.energy += self.food_energy
        else:
            self.move_towards(rabbit)

    def draw(self, canvas):
        canvas.triangle(self.pos, 2.0 * self.radius, self.heading, self.color)


class World:
    def __init__(self, width=800.0, height=600.0):
        self.width = width
        self.height = height
        self.time = 0.0
        self.agents = []

        # Migrants arriving from outside, per second. Without them a species that
        # dies out is gone forever, which happens easily in a small world.
        self.migration = {Rabbit: 0.1, Fox: 0.02}

        self.__newborn = []
        self.__type_cache = {}

    def random_pos(self):
        return Vector2(random.uniform(0.0, self.width), random.uniform(0.0, self.height))

    def populate(self, n_grass=250, n_rabbits=40, n_foxes=6):
        for i in range(n_grass):
            self.agents.append(Grass(self.random_pos()))
        for i in range(n_rabbits):
            self.agents.append(Rabbit(self.random_pos(), random.uniform(5.0, 15.0)))
        for i in range(n_foxes):
            self.agents.append(Fox(self.random_pos(), random.uniform(15.0, 30.0)))

    def random_edge_pos(self):
        if random.random() < 0.5:
            return Vector2(random.choice([0.0, self.width]), random.uniform(0.0, self.height))
        else:
            return Vector2(random.uniform(0.0, self.width), random.choice([0.0, self.height]))

    def add(self, agent):
        # Newborns join after the current step, so the list isn't changed while we loop over it.
        self.__newborn.append(agent)

    def step(self, dt):
        self.__type_cache = {}

        for cls, rate in self.migration.items():
            if random.random() < rate * dt:
                self.add(cls(self.random_edge_pos()))

        for agent in self.agents:
            if agent.alive:
                agent.update(self, dt)

        self.agents = [agent for agent in self.agents if agent.alive] + self.__newborn
        self.__newborn = []
        self.time += dt

    def of_type(self, cls):
        """All agents that are instances of cls, including subclasses of cls."""
        if cls not in self.__type_cache:
            self.__type_cache[cls] = [agent for agent in self.agents if isinstance(agent, cls)]
        return self.__type_cache[cls]

    def count(self, cls):
        return len([agent for agent in self.agents if isinstance(agent, cls) and agent.alive])

    def nearest(self, pos, cls, max_distance, condition=None):
        nearest_agent = None
        nearest_dist2 = max_distance**2

        for agent in self.of_type(cls):
            if not agent.alive or (condition is not None and not condition(agent)):
                continue

            dx = agent.pos.x - pos.x
            dy = agent.pos.y - pos.y
            dist2 = dx*dx + dy*dy

            if dist2 < nearest_dist2:
                nearest_agent = agent
                nearest_dist2 = dist2

        return nearest_agent

    def keep_inside(self, agent):
        if agent.pos.x < agent.radius:
            agent.pos.x = agent.radius
            agent.heading = math.pi - agent.heading
        elif agent.pos.x > self.width - agent.radius:
            agent.pos.x = self.width - agent.radius
            agent.heading = math.pi - agent.heading
        if agent.pos.y < agent.radius:
            agent.pos.y = agent.radius
            agent.heading = -agent.heading
        elif agent.pos.y > self.height - agent.radius:
            agent.pos.y = self.height - agent.radius
            agent.heading = -agent.heading
