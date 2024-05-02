---
title: Asyncio vs Multiprocessing in Python
date: 2024-05-02
categories: [programming, asyncio]
tags: [multiprocessing, asyncio, threading python]
---
    

Asyncio, threading and multiprocessing are three ways to run multiple tasks concurrently in Python. 

## Threading
Best used for I/O-bound tasks. Not suitable for CPU-bound tasks due to the Global Interpreter Lock (GIL) which prevents "true" threading. Lightweight compared to multiprocessing.

## Multiprocessing
Best used for CPU-bound tasks. Creates separate memory spaces for each process. Can utilize multiple CPU cores. More heavyweight than threading and less efficient in terms of memory.

## Asyncio
Best used for I/O-bound tasks. Uses a single thread to run multiple tasks concurrently. More efficient than threading for high volume I/O-bound tasks. 

## Why not always use asyncio instead of threading?
While asyncio is more efficient than threading for I/O-bound tasks, it also introduces complexity. It requires a different programming model (asynchronous programming) and can be more difficult to debug. Threading is simpler to use and understand, and is often sufficient for many use cases.

## Summary Comparison
|Aspect/Feature |	Threading |	Multiprocessing	| asyncio|
|---------------|-------------|-----------------|------|
|Concurrency Model |	Concurrent |	Parallel |	Concurrent|
|Handles CPU-bound	| Poorly (due to GIL)	| Well (true parallelism)	|Poorly|
|Handles I/O-bound |	Well	| Overkill (heavyweight) |	Excellently|
|Memory Efficiency	| Efficient (shared memory)	| Less efficient (separate memory spaces) |	Efficient|

## Asyncio example
```python
import asyncio

async def fetch_data(simulated_delay, name):
    print(f"Starting to fetch data from {name}")
    await asyncio.sleep(simulated_delay)  # Simulate an I/O operation using sleep
    print(f"Finished fetching data from {name}")
    return f"Data from {name}"

async def main():
    # Create a list of tasks
    task1 = asyncio.create_task(fetch_data(2, "Source 1"))
    task2 = asyncio.create_task(fetch_data(3, "Source 2"))
    task3 = asyncio.create_task(fetch_data(1, "Source 3"))

    # Await tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    for result in results:
        print(result)

# Run the event loop
asyncio.run(main())

```