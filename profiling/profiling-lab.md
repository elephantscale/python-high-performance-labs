# Profiling Lab

* Prepare the code and run profiling

## Lab Goals:

1. Prepare and investigate Python code to profile
    * Design the code
    * Make the code run
    
2. Run profiling to determine the possible areas of improvements

3. Implement improvements and measure the results
 
### Builds on:
    * Lecture notes
    
### Time:
    * 1 hour
         
### Step 1) Design the code

* Create a Python mode called `simul.py`
* Create an class to store particle representation

class Particle:

```python
    __slots__ = ('x', 'y', 'ang_speed')

    def __init__(self, x, y, ang_speed):
        self.x = x
        self.y = y
        self.ang_speed = ang_speed
```        