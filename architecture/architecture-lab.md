# Execution Architecture Lab

* Explore how CPython runs your code, and how the memory hierarchy affects speed

## Lab Goals:

1. See the bytecode CPython actually executes
2. Compare two implementations at the bytecode level
3. Measure the effect of cache-friendly memory access

### Builds on:
    * Lecture notes

### Time:
    * 30 min

### Step 1) Disassemble a function with `dis`

* Create a directory `architecture`
* In it, create a file `dis_demo.py`

```python
import dis

def add_with_temp(a, b):
    result = a + b
    return result

def add_direct(a, b):
    return a + b

print("=== add_with_temp ===")
dis.dis(add_with_temp)

print("\n=== add_direct ===")
dis.dis(add_direct)
```

* Run it

```shell script
python dis_demo.py
```

* **Q:** Which function uses fewer bytecode instructions?
* **Q:** The extra `STORE_FAST` / `LOAD_FAST` in `add_with_temp` is the cost of the temporary variable. Tiny here, but in a tight loop it adds up.

### Step 2) Compare two ways to build a list

* Add the following to a new file `loop_vs_comprehension.py`

```python
import dis

def build_loop(n):
    out = []
    for i in range(n):
        out.append(i * i)
    return out

def build_comprehension(n):
    return [i * i for i in range(n)]

print("=== build_loop ===")
dis.dis(build_loop)

print("\n=== build_comprehension ===")
dis.dis(build_comprehension)
```

* Run it and compare

```shell script
python loop_vs_comprehension.py
```

* **Q:** The explicit loop repeatedly does `LOAD_METHOD append` / `CALL`. The comprehension uses a dedicated `LIST_APPEND` opcode and skips the attribute lookup. That is why comprehensions are usually faster.

### Step 3) Feel the memory hierarchy

* Cache-friendly (sequential) access is faster than jumping around memory.
* Create `cache_demo.py`

```python
import time

N = 4000

# Build an N x N matrix as a list of lists
matrix = [[1] * N for _ in range(N)]

# Row-major traversal: walks memory in order (cache-friendly)
start = time.perf_counter()
total = 0
for row in matrix:
    for value in row:
        total += value
row_time = time.perf_counter() - start

# Column-major traversal: jumps between rows (cache-unfriendly)
start = time.perf_counter()
total = 0
for j in range(N):
    for i in range(N):
        total += matrix[i][j]
col_time = time.perf_counter() - start

print(f"Row-major (sequential): {row_time:.3f} s")
print(f"Column-major (strided): {col_time:.3f} s")
print(f"Column-major is {col_time / row_time:.1f}x slower")
```

* Run it

```shell script
python cache_demo.py
```

* **Q:** Both loops do the same number of additions. Why is column-major slower?
* **A:** Row-major access reads memory in the order it is laid out, so the CPU cache is used well. Column-major access jumps around, causing many cache misses.

### Congratulations!

* You can now inspect bytecode and reason about memory access patterns

### Step 4) Bonus lab
* Use `dis.dis` on the `evolve` method from your `simul.py`
* Which instructions run most often (they are inside the inner loop)?
