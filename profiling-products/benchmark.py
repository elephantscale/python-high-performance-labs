from profile_decorator import profile
from simul import ParticleSimulator
from simul import Particle

from random import uniform
import sys

@profile(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def benchmark():
    particles = [Particle(uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0))
                 for i in range(1000)]

    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)

if __name__ == '__main__':
    benchmark()