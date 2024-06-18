---
title: Build Python packages with setuptools or Bazel
date: 2024-06-12
categories: [programming, python, bazel]
tags: [python, bazel, wheel, twine]
---
There are a couple of ways to build Python packages, one of the most common ways is to use `setuptools` to build packages. However, if a python package have more complex dependencies, i.e. you package are importing and using code from another part of a larger repo, building with `Bazel` is one way to handle this in a robust way. In this post, we will look both ways.

## The structure of a Python package
Here is a typical structure of a Python package:
```
my_package_folder/
    my_package/
        __init__.py
        module1.py
        module2.py
    setup.py
    README.md
```
Here I set a different name on the folder containing the package itself. In examples you often see the package folder and the package itself having the same name which can be convenient but I want to illustrate that it is not necessary.


Note the `__init__.py` file in the package folder. This file isn't strictly necessary in Python 3.3 and later, but it can be good practice to include it. The `__init__.py` file can be empty or it can contain initialization code for the package. It's common to use it to expose functions defined in the package modules so that they can be imported directly from the package without having to import the module first. E.g:
By placing
```python
# my_package/__init__.py
from .module1 import my_function
```
in the `__init__.py` file, you can import `my_function` directly from the package like this:
```python
from my_package import my_function
```

Without the `__init__.py` file, you would have to import `my_function` from the `module`:
```python
from my_package.module1 import my_function
```

You can often see two addition files, `LICENSE` and `requirements.txt` in the root folder of the package. The `LICENSE` file contains the license of the package and the `requirements.txt` file contains the dependencies of the package. However, dependencies in the `requirements.txt` file are not used when building the package but can be good to include to explicitly state the dependencies of the package (and easy manual installation). The dependencies that are actually automatically installed when installing the package are defined in the `setup.py` file under `install_requires`. Example:
```python
# setup.py

from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
)
```
`setup()` support many more keyword arguments, see the [documentation](https://setuptools.pypa.io/en/latest/setuptools.html) for more information. Perhaps the most common keyword arguments are:

```python
# setup.py

from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    author='Your Name',
    author_email='your@email.com',
    description='A short description of the package',
    readme='README.md',
    requires_python='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
```
>Note that the package name, i.e. `name='my_package'` doesn't necessarily have to be the same as the folder named `my_package`. The folder name dictate what the import name is when used in an application. The actual package name is what will be shown in e.g. `pip list`. Usually it's conveniant to use the same name.
{: .prompt-info}

`find_packages()` is a function that will automatically find all packages in the package folder and include them. You can specify directories you want to exclude by passing the `exclude` argument to `find_packages()`. E.g. `find_packages(exclude=['tests'])` will exclude the `tests` directory.
`classifiers` is a list of strings that categorize the package. The classifiers are used by the Python Package Index (PyPI) to classify the package. You can find a list of classifiers [here](https://pypi.org/classifiers/).

## Building a Python package with setuptools
To build the python package you need to have `setuptools` (which probably already is installed in your venv) and `wheel` (`pip install wheel`) installed. 

Build the package by running the following command in the root folder of the package:
```bash
python setup.py bdist_wheel
```
which will create a wheel package in the `dist` folder. This wheel package can be installed with `pip install dist/my_package-0.1-py3-none-any.whl`. But if you install a local package you probably want to install in 'editable' mode, i.e. changes in the source code immediately affects the installed package. This can be done by running `pip install -e .` in the root folder of the package (or instead of `.` providing the path to the package).

You can also package the source code by running `python setup.py sdist` which will create a tarball with the source code in the `dist` folder.

## Pushing the package to a package index

To make the package available to others you can push the package to a package index. The most common package index is the Python Package Index (PyPI). If you are working in a company you might have an internal package index in e.g. an Artifactory or Nexus repository. To push the package you can use the `twine` package. Install `twine` by running `pip install twine`. 

To specify the url, user and password when pushing to an internal package index you can create a `.pypirc` file in your home directory. Something like this: 

```ini
[distutils]
index-servers =
  artifactory

[artifactory]
repository: https://your-artifactory-domain/artifactory/api/pypi/your-repository-name

```
however, if this is in a ci pipe line you probably want to specify the user and password as environment variables.
```bash
export TWINE_USERNAME=your-username
export TWINE_PASSWORD=your-password
```
Then you can push the package by running:
```bash
twin repository-url https://your-artifactory-domain/artifactory/api/pypi/your-repository-name dist/*
```
where you specify url directly in the command. 
You can actually set the url as an environment variable as well:
```bash
export TWINE_REPOSITORY_URL=https://your-artifactory-domain/artifactory/api/pypi/your-repository-name
```
and then push whith this command:
```bash
twin dist/*
```


## Building a Python package with Bazel (TO BE EXPANDED AND IMPROVED)
To build with Bazel you need to have Bazel installed. If you don't have Bazel installed you can follow the instructions [here](https://docs.bazel.build/versions/main/install.html).

The first thing you need to do is to create a `BUILD` file in the root folder of the package. The `BUILD` file is used by Bazel to build the package. Here is an example of a `BUILD` file:
```python
# BUILD

load("@rules_python//python:defs.bzl", "py_library", "py_binary")

py_library(
    name = "my_package",
    srcs = glob(["my_package/**/*.py"]),
    deps = [
        "//path/to/dependency1",
        "//path/to/dependency2",
    ],
)

py_binary(
    name = "my_package_binary",
    srcs = ["my_package/main.py"],
    deps = [":my_package"],
)
```

Now you can build the package by running:
```bash
bazel build //path/to/package:my_package_binary
```

This will create a binary in the `bazel-bin` folder. You can run the binary by running:
```bash
bazel-bin/path/to/package/my_package_binary
```
This will run the `main.py` file in the package.

To build a wheel package you can use the `py_binary` rule in the `BUILD` file. Here is an example of a `BUILD` file that builds a wheel package:
```python

# BUILD

load("@rules_python//python:defs.bzl", "py_library", "py_binary", "py_wheel")

py_library(
    name = "my_package",
    srcs = glob(["my_package/**/*.py"]),
    deps = [
        "//path/to/dependency1",
        "//path/to/dependency2",
    ],
)

py_wheel(
    name = "my_package_wheel",
    srcs = [":my_package"],
    deps = [":my_package"],
)

```


Note that dependencies don't need to be placed in the same folder as the package. You can specify the path to the dependency by using the `//` syntax. E.g. `//path/to/dependency1` specifies that the dependency is in the root folder of the repo.
The advantage of building with Bazel is that you can build a package that is part of a larger repo and that you can specify dependencies that are not part of the package itself. This can be useful if you are building a package that is part of a larger repo and you want to use code from other parts of the repo in the package.
