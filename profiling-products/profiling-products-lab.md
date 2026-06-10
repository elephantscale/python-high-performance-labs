# Profiling Lab

### This is an optional lab for the "High Performance Python" course

### Step 1: Run the V1 of the code

Create the file `product_counter_v1.py`

```python
from profile_decorator import profile
import random

random.seed(20)


def create_products(num):
    """Create a list of random products with 3-letter alphanumeric name."""
    return [''.join(random.choices('ABCDEFG123', k=3)) for _ in range(num)]

def create_counter(products):
    counter_dict = {}
    for p in products:
        if p not in counter_dict:
            counter_dict[p] = 0
        counter_dict[p] += 1
    return counter_dict

def sort_counter(counter_dict):
    return {k: v for k, v in sorted(counter_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}



@profile(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def product_counter_v1(products):
    """Get count of products in descending order."""
    counter_dict = create_counter(products)
    sorted_p = sort_counter(counter_dict)
    return sorted_p

if __name__ == '__main__':
    num = 1_000_000  # assume we have sold 1,000,000 products
    products = create_products(num)
    counter_dict1 = product_counter_v1(products)  # profile v1
```




* We are going to profile the performance.

* Go ahead and run `python product_counter_v1.py`.  

* You should get an output in the file `product_counter_v1.prof`

```console
         1007 function calls in 0.206 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.206    0.206 profile_decorator.py:70(product_counter_v1)
        1    0.191    0.191    0.191    0.191 profile_decorator.py:87(create_counter)
        1    0.000    0.000    0.015    0.015 profile_decorator.py:106(sort_counter)
        1    0.015    0.015    0.015    0.015 {built-in method builtins.sorted}
        1    0.000    0.000    0.000    0.000 profile_decorator.py:107(<dictcomp>)
     1000    0.000    0.000    0.000    0.000 profile_decorator.py:108(<lambda>)
        1    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

```

Q: Where are we spending the most time?
A: in `create_couter`

### Step 2: Make a version 2 of the file

We are going to make a slightly better version of the code, and will profile it.

**TODO: Make a file called `product_coutner_v2.py`**


```python
from profile_decorator import profile
import random

random.seed(20)


def create_products(num):
    """Create a list of random products with 3-letter alphanumeric name."""
    return [''.join(random.choices('ABCDEFG123', k=3)) for _ in range(num)]

def sort_counter(counter_dict):
    return {k: v for k, v in sorted(counter_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}


def create_counter_v2(products):
    counter_dict = {}
    for p in products:
        try:
            counter_dict[p] += 1
        except KeyError:
            counter_dict[p] = 1
    return counter_dict


@profile(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def product_counter_v2(products):
    """Get count of products in descending order."""
    counter_dict = create_counter_v2(products)
    sorted_p = sort_counter(counter_dict)
    return sorted_p


if __name__ == '__main__':
    num = 1_000_000  # assume we have sold 1,000,000 products
    products = create_products(num)
    counter_dict1 = product_counter_v2(products)
```

You should get an output in the file `product_counter_v2.prof`

**TODO: see the output in file `product_counter_v2.prof`**

** Q: Why is the V2 faster than the V1?**
** A: create_counter_v2 is implemented more efficiently


### Step 3: Edit the file to run V3

* In version 3, we will be using the python collections.counter which is faster.

* Create the file `product_counter_v3.py`

```python
from profile_decorator import profile
import random
import collections

random.seed(20)


def create_products(num):
    """Create a list of random products with 3-letter alphanumeric name."""
    return [''.join(random.choices('ABCDEFG123', k=3)) for _ in range(num)]

def sort_counter(counter_dict):
    return {k: v for k, v in sorted(counter_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}

# version3
@profile(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def product_counter_v3(products):
    """Get count of products in descending order."""
    return collections.Counter(products)


if __name__ == '__main__':
    num = 1_000_000  # assume we have sold 1,000,000 products
    products = create_products(num)
    counter_dict1 = product_counter_v3(products)
```

**TODO: Run `python product_counter_v3.py`**

**TODO: see the output in file `product_counter_v3.prof`**

* Q: Why did that one seem to run better?
* A: product_counter_v3 is using a Counter object in the collections library


### Step 3: Bonus lab
* Add profile decorator to the `benchmark.py`