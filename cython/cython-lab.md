# Cython Lab

> **Lab tier — demo:** your instructor runs this live; hands-on is optional/take-home.

* Compile a hot function to native code and measure the speedup

## Lab Goals:

1. Install Cython
2. Move the particle evolve loop into a `.pyx` module
3. Add static types for a real speedup
4. Build the extension and benchmark it

### Builds on:
    * The NumPy lab (we reuse the array packing)
    * Lecture notes

### Time:
    * 40 min

### Step 0) Install Cython

```shell script
pip install cython numpy
```

* You also need a C compiler
    * Linux: `gcc` (usually `sudo apt install build-essential`)
    * macOS: Xcode command line tools (`xcode-select --install`)
    * Windows: the Microsoft C++ Build Tools

### Step 1) Write the Cython module

* Create a directory `cython`
* Create a file `cevolve.pyx`

```python
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def c_evolve(double[:, :] r_i,
             double[:] ang_speed_i,
             double timestep,
             int nsteps):

    cdef int i, j
    cdef int nparticles = r_i.shape[0]
    cdef double norm, vx, vy, dx, dy, x, y

    for i in range(nsteps):
        for j in range(nparticles):
            x = r_i[j, 0]
            y = r_i[j, 1]

            norm = (x * x + y * y) ** 0.5
            vx = -y / norm
            vy = x / norm

            dx = timestep * ang_speed_i[j] * vx
            dy = timestep * ang_speed_i[j] * vy

            r_i[j, 0] = x + dx
            r_i[j, 1] = y + dy
```

* The `cdef` declarations and typed memoryviews (`double[:, :]`) are what make this fast.

### Step 2) Write the build script

* Create `setup.py`

```python
from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("cevolve.pyx"),
    include_dirs=[np.get_include()],
)
```

### Step 3) Build the extension

```shell script
python setup.py build_ext --inplace
```

* This generates `cevolve.c` and a compiled module (e.g. `cevolve.*.so`).

### Step 4) Use and benchmark it

* Create `run_cython.py`

```python
import time
import numpy as np
from random import uniform
from cevolve import c_evolve

def pure_python_evolve(r_i, ang_speed_i, timestep, nsteps):
    nparticles = r_i.shape[0]
    for i in range(nsteps):
        for j in range(nparticles):
            x = r_i[j, 0]
            y = r_i[j, 1]
            norm = (x * x + y * y) ** 0.5
            vx = -y / norm
            vy = x / norm
            r_i[j, 0] = x + timestep * ang_speed_i[j] * vx
            r_i[j, 1] = y + timestep * ang_speed_i[j] * vy

def make_arrays(n):
    r_i = np.array([[uniform(-1.0, 1.0), uniform(-1.0, 1.0)] for _ in range(n)])
    ang_speed_i = np.array([uniform(-1.0, 1.0) for _ in range(n)])
    return r_i, ang_speed_i

if __name__ == '__main__':
    n, timestep, nsteps = 1000, 0.00001, 10000

    r_i, ang = make_arrays(n)
    start = time.perf_counter()
    pure_python_evolve(r_i, ang, timestep, nsteps)
    py = time.perf_counter() - start

    r_i, ang = make_arrays(n)
    start = time.perf_counter()
    c_evolve(r_i, ang, timestep, nsteps)
    cy = time.perf_counter() - start

    print(f"pure python: {py:.3f} s")
    print(f"cython:      {cy:.3f} s")
    print(f"cython is {py / cy:.1f}x faster")
```

* Run it

```shell script
python run_cython.py
```

* **Q:** How much faster is the Cython version than the pure-Python loop doing the exact same math?

### Congratulations!

* You compiled Python to native code and measured a real speedup

### Step 5) Bonus lab
* Run `cython -a cevolve.pyx` to generate `cevolve.html`
* Yellow lines are where Cython still calls back into Python — try to make the hot loop "whiter"
