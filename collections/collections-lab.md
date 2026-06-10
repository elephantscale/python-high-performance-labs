# Collections Lab

* Pick the right data structure and measure the difference

## Lab Goals:

1. Compare list vs set membership testing
2. Compare list vs deque for queue operations
3. Use a heap to get the top-k items
4. Cache expensive calls with `lru_cache`
5. Save memory with `__slots__`

### Builds on:
    * Lecture notes
    * Execution architecture lab

### Time:
    * 40 min

### Step 1) List vs set membership

* Create a directory `collections`
* Create a file `membership.py`

```python
import time

N = 100_000
data_list = list(range(N))
data_set = set(data_list)

# Look up values that are NOT present (worst case for a list)
lookups = [N + i for i in range(1000)]

start = time.perf_counter()
for x in lookups:
    x in data_list          # O(n) each time
list_time = time.perf_counter() - start

start = time.perf_counter()
for x in lookups:
    x in data_set           # O(1) each time
set_time = time.perf_counter() - start

print(f"list membership: {list_time:.4f} s")
print(f"set  membership: {set_time:.4f} s")
print(f"set is {list_time / set_time:.0f}x faster")
```

* Run it

```shell script
python membership.py
```

* **Q:** Why is the set so much faster?
* **A:** `in` on a list scans every element (O(n)); a set uses a hash table (O(1)).

### Step 2) List vs deque as a queue

* Create `queue_demo.py`

```python
import time
from collections import deque

N = 200_000

# Using a list as a queue: pop(0) is O(n)
lst = list(range(N))
start = time.perf_counter()
while lst:
    lst.pop(0)
list_time = time.perf_counter() - start

# Using a deque: popleft() is O(1)
dq = deque(range(N))
start = time.perf_counter()
while dq:
    dq.popleft()
deque_time = time.perf_counter() - start

print(f"list.pop(0):    {list_time:.4f} s")
print(f"deque.popleft(): {deque_time:.4f} s")
print(f"deque is {list_time / deque_time:.0f}x faster")
```

* Run it

```shell script
python queue_demo.py
```

* **Q:** Removing from the front of a list shifts every other element. A deque does not.

### Step 3) Top-k with a heap

* Create `topk.py`

```python
import heapq
import random

random.seed(20)
data = [random.randint(0, 1_000_000) for _ in range(100_000)]

# Get the 10 largest values efficiently
top10 = heapq.nlargest(10, data)
print("Top 10:", top10)

# A min-heap always keeps the smallest item at the front
h = []
for value in data[:20]:
    heapq.heappush(h, value)
print("Smallest of first 20:", heapq.heappop(h))
```

* Run it

```shell script
python topk.py
```

* **Q:** `heapq.nlargest(k, data)` is O(n log k) — much cheaper than sorting the whole list when k is small.

### Step 4) Caching with lru_cache

* Create `caching.py`

```python
import time
from functools import lru_cache

def fib_slow(n):
    if n < 2:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

@lru_cache(maxsize=None)
def fib_fast(n):
    if n < 2:
        return n
    return fib_fast(n-1) + fib_fast(n-2)

start = time.perf_counter()
fib_slow(32)
print(f"fib_slow(32): {time.perf_counter() - start:.4f} s")

start = time.perf_counter()
fib_fast(32)
print(f"fib_fast(32): {time.perf_counter() - start:.6f} s")
print("cache stats:", fib_fast.cache_info())
```

* Run it

```shell script
python caching.py
```

* **Q:** The slow version recomputes the same subproblems exponentially. The cache stores each result once.

### Step 5) Memory savings with __slots__

* Create `slots_demo.py`

```python
import sys

class ParticleDict:
    def __init__(self, x, y, ang_speed):
        self.x = x
        self.y = y
        self.ang_speed = ang_speed

class ParticleSlots:
    __slots__ = ('x', 'y', 'ang_speed')
    def __init__(self, x, y, ang_speed):
        self.x = x
        self.y = y
        self.ang_speed = ang_speed

p1 = ParticleDict(1.0, 2.0, 0.5)
p2 = ParticleSlots(1.0, 2.0, 0.5)

# A normal instance carries a __dict__; a slotted one does not
print("with __dict__:", sys.getsizeof(p1) + sys.getsizeof(p1.__dict__), "bytes")
print("with __slots__:", sys.getsizeof(p2), "bytes")
```

* Run it

```shell script
python slots_demo.py
```

* **Q:** With millions of particles, `__slots__` can save a large amount of memory.

### Congratulations!

* You can now choose data structures that match your access patterns

### Step 6) Bonus lab
* In your particle `simul.py`, add `__slots__` to the `Particle` class
* Re-run the timing lab — does the benchmark change?
