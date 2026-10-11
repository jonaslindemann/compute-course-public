# -*- coding: utf-8 -*-

import random

import matplotlib.pyplot as plt

from ecosystem import World, Rabbit, Fox

random.seed(0)    # remove this line to get a different ecosystem every run

DT = 0.1          # seconds per simulation step
SIM_TIME = 600.0  # seconds to simulate

world = World()
world.populate()

times = []
rabbits = []
foxes = []

step = 0

while world.time < SIM_TIME:
    world.step(DT)
    step += 1

    if step % 5 == 0:
        times.append(world.time)
        rabbits.append(world.count(Rabbit))
        foxes.append(world.count(Fox))

    if step % 1000 == 0:
        print("t =", round(world.time), "s, rabbits:", rabbits[-1], "foxes:", foxes[-1])

fig, (ax_time, ax_phase) = plt.subplots(1, 2, figsize=(12, 4.5))

ax_time.plot(times, rabbits, color="tab:blue", label="Rabbits")
ax_time.plot(times, foxes, color="tab:orange", label="Foxes")
ax_time.set_xlabel("Time [s]")
ax_time.set_ylabel("Population")
ax_time.set_title("Populations over time")
ax_time.legend()

ax_phase.plot(rabbits, foxes, color="tab:gray", linewidth=0.8)
ax_phase.set_xlabel("Rabbits")
ax_phase.set_ylabel("Foxes")
ax_phase.set_title("Rabbits vs. foxes")

fig.tight_layout()
plt.show()
