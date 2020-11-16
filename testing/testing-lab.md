# Testing Lab

* Prepare the tests for the code, lay the foundation for optimization

## Lab Goals:

1. Prepare Python code tests
    * Add tests
    
### Builds on:
    * Modeling lab    
[Modeling lab](../modeling/modeling-lab.md)    
    * Lecture notes
    
### Time:
    * 30 min

### Step 1) Create a new `testing` directory         

* Work in the new `testing` directory
* Create a Python module `test_evolve.py` 

### Step 2) Continue building on `simul.py`

* To avoid Python import complications, copy `simul.py` into the new `testing`
* To import the `simul` module, add the following to the `test_evolve.py`:

```python
from simul import ParticleSimulator
from simul import Particle
```          
### Step 3) Write the test code
* Add the following code into `test_evolve.py`:

```python

def test_evolve():
    particles = [Particle(0.3, 0.5, +1),
                 Particle(0.0, -0.5, -1),
                 Particle(-0.1, -0.4, +3)]

    simulator = ParticleSimulator(particles)

    simulator.evolve(0.1)

    p0, p1, p2 = particles

    def fequal(a, b, eps=1e-5):
        return abs(a - b) < eps

    assert fequal(p0.x, 0.210269)
    assert fequal(p0.y, 0.543863)

    assert fequal(p1.x, -0.099334)
    assert fequal(p1.y, -0.490034)

    assert fequal(p2.x, 0.191358)
    assert fequal(p2.y, -0.365227)
# uncomment the line below and verify that you get an error
#    assert fequal(p2.y, -1.365227)


if __name__ == '__main__':
    test_evolve()
    print("test_evolve ran")
    print("did you get any errors?")
```

### Step 4) Run the test
```shell script
python test_evolve.py
```
* Verify that you did not get any errors and that the output of the program confirms it

### Step 5) Make the test fail

* Change some number in the asserts. Run the test again and verify that it now fails
* Revert the changes and verify that the tests works again

### Step 6) Congratulations! 

* You have a added the tests to run when you are going to do your optimizations
