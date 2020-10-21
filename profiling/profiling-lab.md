# Profiling Lab

* Learn how to run profile

## Lab Goals:

1. Use the existing code to profile and find bottlenecks
    * Copy the code
    * Run benchmark
    * Profile Python code
    
### Builds on:
    * Previous labs
    
### Time:
    * 30 hour
         
### Step 1) Prepare the code for profiling 

* Create a new directory, `profiling`
* Copy the modules, `simul.py` and `benchmark.py` into this directory
          
### Step 2) Run profiling

* On the command line, in this directory, run
```shell script
python -m cProfile benchmark.py
```
* Analyze the output
    * Q: Which function took the most time?
    * It is `simul.py:19(evolve)` but it is hard to see
    
* Run the profiler sorting the results by `tottime`

```shell script
python -m cProfile -s tottime benchmark.py
```    
* Analyze the output
    * Q: Which function took the most time?
    * It is `simul.py:19(evolve)` and it is easier to see
    
### Step 2) Save profiling output into a file

* Create a new file, `taylor.py`
```python
def factorial(n):
    if n == 0:
        return 1.0
    else:
        return n * factorial(n - 1)


def taylor_exp(n):
    return [1.0 / factorial(i) for i in range(n)]


def taylor_sin(n):
    res = []
    for i in range(n):
        if i % 2 == 1:
            res.append((-1) ** ((i - 1) / 2) / float(factorial(i)))
        else:
            res.append(0.0)
    return res


def benchmark():
    taylor_exp(500)
    taylor_sin(500)


if __name__ == '__main__':
    benchmark()
```
* Create a profiler output file
```shell script
python -m cProfile -o prof.out taylor.py
```  
* Prepare to analyze profiler output
```shell script
pyprof2calltree -i prof.out -o prof.calltree
```  

* Use `KCachegrind` to see the output
```shell script
kcachegrind prof.calltree
```
* (If you don't have it, do `pip install pyprof2calltree`)

* Observe the output of KCachegrind
![](../artwork/kcachegrind.png)

### Step 3) Improvements

### Step 4 ) Test improvements

* Run the timing for the previous benchmark

```shell script
time python benchmark.py
```         

* Your results will be something like the following
```text
real    0m4.773s
user    0m4.729s
sys     0m0.044s

```

Now run the "fast" results and check how fast they are
```shell script
time python benchmark_fast.py
```         

* You should get someting like
```text
real    0m3.980s
user    0m3.938s
sys     0m0.041s


```

## Congratulation!
* You have achieved 20% improvements!