# NumPy Lab

* Rewrite the particle simulator with NumPy and measure the speedup

## Lab Goals:

1. Get comfortable with NumPy arrays and vectorization
2. Convert the `evolve` loop to a vectorized `evolve_numpy`
3. Benchmark pure Python vs NumPy
4. Visualize the benchmark and speedup with matplotlib

### Builds on:
    * The modeling and timing labs (the particle simulator)
    * Lecture notes

### Time:
    * 40 min

### Step 0) Install NumPy

```shell script
pip install numpy
```

### Step 1) NumPy warm-up

* Create a directory `numpy`
* Create a file `numpy_intro.py`

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])

print("a + b   =", a + b)
print("a * 2   =", a * 2)
print("a . b   =", a.dot(b))
print("a sum   =", a.sum())

# A 2D array: each row is a particle's (x, y)
r = np.array([[0.3, 0.5],
              [0.0, -0.5],
              [-0.1, -0.4]])
norm = np.sqrt((r ** 2).sum(axis=1))   # per-row norm via broadcasting
print("norms   =", norm)
```

* Run it

```shell script
python numpy_intro.py
```

### Step 2) Add a vectorized `evolve_numpy`

* Copy your `simul.py` from the modeling lab into the `numpy` directory
* Add `import numpy as np` at the top
* Add this method to the `ParticleSimulator` class

```python
    def evolve_numpy(self, dt):
        timestep = 0.00001
        nsteps = int(dt / timestep)

        # Pack particle state into arrays
        r_i = np.array([[p.x, p.y] for p in self.particles])
        ang_speed_i = np.array([p.ang_speed for p in self.particles])

        for i in range(nsteps):
            norm_i = np.sqrt((r_i ** 2).sum(axis=1))

            # v = (-y, x) / norm   -- the direction of motion
            v_i = r_i[:, [1, 0]].copy()
            v_i[:, 0] *= -1
            v_i /= norm_i[:, np.newaxis]

            d_i = timestep * ang_speed_i[:, np.newaxis] * v_i
            r_i += d_i

        # Write the results back into the particle objects
        for i, p in enumerate(self.particles):
            p.x, p.y = r_i[i]
```

* Note: the inner loop over particles is gone — NumPy handles all particles at once.

### Step 3) Verify the two methods agree

* Create `test_numpy.py`

```python
from simul import Particle, ParticleSimulator

def fequal(a, b, eps=1e-5):
    return abs(a - b) < eps

def test_evolve_numpy():
    particles = [Particle(0.3, 0.5, +1),
                 Particle(0.0, -0.5, -1),
                 Particle(-0.1, -0.4, +3)]
    simulator = ParticleSimulator(particles)
    simulator.evolve_numpy(0.1)

    p0, p1, p2 = particles
    assert fequal(p0.x, 0.210269)
    assert fequal(p0.y, 0.543863)
    print("evolve_numpy matches the reference values")

if __name__ == '__main__':
    test_evolve_numpy()
```

* Run it

```shell script
python test_numpy.py
```

### Step 4) Benchmark pure Python vs NumPy

* Create `benchmark_numpy.py`

```python
import time
from random import uniform
from simul import Particle, ParticleSimulator

def make_particles(n):
    return [Particle(uniform(-1.0, 1.0),
                     uniform(-1.0, 1.0),
                     uniform(-1.0, 1.0)) for _ in range(n)]

def benchmark(n, method):
    particles = make_particles(n)
    simulator = ParticleSimulator(particles)
    start = time.perf_counter()
    getattr(simulator, method)(0.1)
    return time.perf_counter() - start

if __name__ == '__main__':
    for n in (100, 1000):
        py = benchmark(n, 'evolve')
        np_ = benchmark(n, 'evolve_numpy')
        print(f"n={n:5d}  python={py:.3f}s  numpy={np_:.3f}s  speedup={py/np_:.1f}x")
```

* Run it

```shell script
python benchmark_numpy.py
```

* **Q:** For which particle count does NumPy win the most?
* **A:** NumPy has per-call overhead, so its advantage grows as the number of particles grows.

### Step 5) Visualize the benchmark

* A chart makes the speedup obvious in a way a table of numbers does not
* Create `plot_benchmark.py`

```python
import matplotlib.pyplot as plt
from benchmark_numpy import benchmark

sizes = [100, 300, 1000]            # add 3000 for a stronger curve (slower)
python_times, numpy_times = [], []
for n in sizes:
    python_times.append(benchmark(n, 'evolve'))
    numpy_times.append(benchmark(n, 'evolve_numpy'))

speedup = [p / q for p, q in zip(python_times, numpy_times)]

# Runtime curves: pure Python vs NumPy
plt.figure()
plt.plot(sizes, python_times, 'o-', label='pure Python')
plt.plot(sizes, numpy_times, 's-', label='NumPy')
plt.xlabel('number of particles'); plt.ylabel('runtime (s)')
plt.title('Runtime vs problem size'); plt.legend()
plt.savefig('benchmark.png')

# Speedup bar chart
plt.figure()
plt.bar([str(n) for n in sizes], speedup, color='green')
plt.xlabel('number of particles'); plt.ylabel('speedup (x)')
plt.title('NumPy speedup grows with problem size')
plt.savefig('speedup.png')

plt.show()
```

* Run it

```shell script
python plot_benchmark.py
```

* Open `benchmark.png` and `speedup.png`
* **Q:** What happens to the speedup bars as the number of particles grows?
* **A:** They get taller — NumPy's advantage widens with scale, because its
  per-call overhead is amortized over more work.

### Congratulations!

* You vectorized a real simulation loop with NumPy — and visualized the payoff

### Step 6) Bonus lab
* Profile `evolve_numpy` with `cProfile` (from the profiling lab)
* Which NumPy calls dominate the time now?
