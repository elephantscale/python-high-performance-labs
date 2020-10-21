# Time Lab

* Exercise with timing the running code

## Lab Goals:

1. Get familiar with running the timing command
    
### Builds on:
    * Previous labs
    * Lecture notes
    
### Time:
    * 1 hour

### Step 1) Time the benchmark.py module
* Prepare a new directory, `timing
* Copy the modulea `simul.py` and `benchmark.py` into this directory
* On the command line, run the `time` command
 
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

### Step 2) Use IPython
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

* Note that the last command will take a long time
* Observe the result similar to the one below
```text
4.33 s ± 10.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

```

### Step 3) Bonus lab
* Write a Jupyter Notebook for the IPython shell above
* It will work there as well

### Windows user advice

The `time` command is not available for Windows. 

To install Unix tools, such as time, on Windows you can use the cygwin shell, 
downloadable from the official website 
(http://www.cygwin.com/).
 
Alternatively, you can use similar PowerShell commands, such as Measure-Command 
(https://msdn.microsoft.com/en-us/powershell/reference/5.1/microsoft.powershell.utility/measure-command). 

