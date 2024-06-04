---
title: Using C/C++ shared objects in Python
date: 2024-05-31
categories: [programming, python, c++, c]
tags: [python, c++, c, shared objects, ctypes, pybind11]
---
    
It's quite common for Python modules to be written partly in C or C++ for performance reasons. One way to do this is to use "shared objects" in Python. In this post, we will look at two ways to do this:: using the `ctypes` module, and using `pybind11`. Depending on the situation this might be easier than using e.g. Cython.

## Using ctypes

Let's look at a simple example. Create the file `add.c` with the following content:
```c
float add(float a, float b) {
    return a + b;
}
```
<br>

Compile the file with the following command:
```bash
gcc -shared -o libadd.so -fPIC add.c
```
which ceates a shared object file `add.so`.
<br>

Create a Python script in the same directory with the following content:
```python
import ctypes

# Load the shared library
lib = ctypes.CDLL('./libadd.so')

# Set the argument and result types
lib.add.argtypes = [ctypes.c_float, ctypes.c_float] # notice c_float. If we e.g. used integers, we would use ctypes.c_int
lib.add.restype = ctypes.c_float

# Function to add two floats
def add_floats(x, y):
    return lib.add(x, y)

# Example usage
result = add_floats(5.5, 4.5)
print("The result is:", result)
```


(This simple function will probably not be faster then the built-in `+` operator in Python because of the function call overhead which in this case will take much longer than the actual computation. But it's a simple example to show how to use shared objects in Python.)

## Using pybind11
When importing shared objects from c++ code `ctypes`  can stillb e utilized, but it has several limitations. Instead, let's use `pybind11`.
First install `pybind11` with the following command:
```bash
pip install pybind11
```

Create a file `add.cpp` with the following content:
```cpp
#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("add", &add, "A function which adds two numbers", py::arg("i"), py::arg("j"));
}
```
Notice that we could add a module docstring, function docstring and argument names to the function.
<br>

Compile the file with the following command:
```bash
c++ -O3 -Wall -shared -std=c++14 -fPIC $(python3 -m pybind11 --includes) example.cpp -o example$(python3-config --extension-suffix)
```
This will create a shared object file with name something like `example.cpython-310-x86_64-linux-gnu.so`

Create a Python script in the same directory with the following content:
```python
import example

print("The result is:", example.add(5, 4))
```
Sometime the docstring will not show in the IDE, but you can still access it (the whole module) with `help(example)` or `example.__doc__`, or for the function `help(example.add)` or `example.add.__doc__`.

<br>

So there is quite a small overhead in using shared objects in Python, and also quite easy to get started. 