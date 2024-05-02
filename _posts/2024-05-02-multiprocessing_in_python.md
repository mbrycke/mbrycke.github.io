---
title: Multiprocessing in Python
date: 2024-05-02
categories: [programming, multiprocessing]
tags: [multiprocessing, python]
---
    
## Introduction
To run multiple tasks concurrently without using threads (which is limited by the GIL), we can use the `multiprocessing` module in Python. The `multiprocessing` module allows us to create multiple processes, each with its own memory space *and* its own Python interpreter. This means that the processes can run in parallel and possibly utilize multiple CPU cores. If you have a CPU-bound task, multiprocessing is a good choice.

## Example
```python
import multiprocessing
import time

def cpu_bound_task(x):
    count = 0
    for i in range(int(1e8)):
        count += i
    return count

if __name__ == "__main__":
    start_time = time.time()

    inputs = [1, 2, 3, 4]

    # Create a pool of processes
    with multiprocessing.Pool() as pool:
        # Map cpu_bound_task to the inputs and execute in parallel
        results = pool.map(cpu_bound_task, inputs)

    print(f"Time taken: {time.time() - start_time} seconds")
    print("Results:", results)

```
yields
```bash
Time taken: 1.7265195846557617 seconds
Results: [4999999950000000, 4999999950000000, 4999999950000000, 4999999950000000]
```

and without multiprocessing
```python
import time

def cpu_bound_task():
    count = 0
    for i in range(int(1e8)):
        count += i
    return count

if __name__ == "__main__":
    start_time = time.time()

    results = []
    for i in inputs:
        results.append(cpu_bound_task(i))

    print(f"Time taken: {time.time() - start_time} seconds")
    print("Results:", results)
```
yields
```bash
Time taken: 6.604349136352539 seconds
Results: [4999999950000000, 4999999950000000, 4999999950000000, 4999999950000000]
```
So quite a bit faster with multiprocessing.

However, there is an overhead in creating processes. If we would set the counter to `int(1e4)` instead of `int(1e8)` the overhead would probably make the multiprocessing version slower.