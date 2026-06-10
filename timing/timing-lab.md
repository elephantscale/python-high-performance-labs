# Timing Lab

> **Lab tier — demo:** your instructor runs this live; watching is enough.

* Exercise with benchmarking and timing the running code

## Lab Goals:

* Get familiar with running the timing command
    
### Builds on:
    * Previous labs
    * Lecture notes
    
### Time:
    * 30 min

### Step 1) Prepare the `benchmark.py` module
* Prepare a new directory, called `timing`
* Copy the module `simul.py` into this directory
* Create a file `benchmark.py` in this directory
* Add the following to `benchmark.py`

```python
from simul import ParticleSimulator
from simul import Particle
from random import uniform 

def benchmark(): 
    particles = [Particle(uniform(-1.0, 1.0), 
                          uniform(-1.0, 1.0), 
                          uniform(-1.0, 1.0)) 
                  for i in range(1000)] 

    simulator = ParticleSimulator(particles) 
    simulator.evolve(0.1) 

if __name__ == '__main__': 
    benchmark()
```
* Run the `benchmark.py` module and verify that it runs

```shell script
python benchmark.py
```

* You can verify the load on the system, with a display similar to the one below, 
but perhaps using your own way of watching the load

 ![](../artwork/load.png)
 
### Step 2) Time the benchmark.py module

* On the command line, run the timing command
 
```shell script
time python benchmark.py
```         
* (If you are in Windows, see advice at the end of the lab)
* You will get an output similar to the one below

```text
real    0m4.614s
user    0m4.589s
sys     0m0.025s

```

* Can you explain what each of the three timings measures?

### Step 3) Use IPython
* If you do not have it, install IPython

```shell script
$ pip install ipython
```

* Start IPython shell

```shell script
$ ipython
```

In the IPython shell, issue two commands

```shell script
from benchmark import benchmark 
%timeit benchmark() 
```

* **Note that the last command will take a long time**

* Observe the result similar to the one below
```text
4.33 s ± 10.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

```

### Congratulations!

* You can time your Python code now

### Step 4) Bonus lab
* Write a Jupyter Notebook for the IPython shell above
* Timing will work there as well

### Windows user advice

The `time` command is not available for Windows. 

To install Unix tools, such as time, on Windows you can use the cygwin shell, 
downloadable from the official website 
(http://www.cygwin.com/).
 
Alternatively, you can use similar PowerShell commands, such as Measure-Command 
(https://msdn.microsoft.com/en-us/powershell/reference/5.1/microsoft.powershell.utility/measure-command). 

