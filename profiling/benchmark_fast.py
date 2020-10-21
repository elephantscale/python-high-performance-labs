from simul_fast import ParticleSimulator
from simul_fast import Particle

from random import uniform
import sys

def benchmark():
    particles = [Particle(uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0))
                 for i in range(1000)]

    simulator = ParticleSimulator(particles)
    simulator.evolve_fast(0.1)

if __name__ == '__main__':
    benchmark()