---
title: The enum module in Python
date: 2024-05-30
categories: [programming, python]
tags: [enum, flag, auto]
---
    
Using the enum module in Python can make the code more readable and also help with autocompletion in IDEs (e.g. lessen risk for typos etc.) It's useful for e.g. replacing magic numbers  or in switch/case statements, if statements etc.

Example:
```python
import enum

class Color(enum.Enum):
    RED = 1 # uppercase is used for enum values
    GREEN = 2
    BLUE = 3


def print_color(color: Color):
    if color == Color.RED:
        print("Red")
    elif color == Color.GREEN:
        print("Green")
    elif color == Color.BLUE:
        print("Blue")
    else:
        print("Unknown color")
```

You get the name and value of the enum like this:
```python
name = Color.RED.name # 'RED'
value = Color.RED.value # 1
```

If an enum doesn't need a particular value you can use `auto()` to automatically assign a value:
```python

class Color(enum.Enum):
    RED = enum.auto()
    GREEN = enum.auto()
    BLUE = enum.auto()
```
Values will be assigned in the order they are defined, starting from 1.

<br>

To iterate over the enum values you can do like this:
```python
for color in Color:
    print(color) # Color.RED, Color.GREEN, Color.BLUE
```
<br>

You can also use the `__members__` attribute to get a dictionary of the enum values:
```python
for name, value in Color.__members__.items():
    print(name, value) # RED 1, GREEN 2, BLUE 3
```

## Flag enums
Perhaps a bit more esoteric is the use of flag enums. This allows you to combine the values using bitwise operators. This can be useful when you want to represent a set of flags, add or remove flags etc.

Example:
```python
class Permission(Flag): # Flag is a subclass of Enum that 
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

# Check combined permissions
my_permissions = Permission.READ | Permission.WRITE 

# Check if a permission is set
if Permission.READ in my_permissions: # or my_permissions & Permission.READ. Both are same, however the former is more readable but the latter is more efficient. Generally we go for the more readable one since when using python we are generally more concerned about readability than efficiency.
    print("Permission.READ is set")

if Permission.EXECUTE in my_permissions:
    print("Permission.EXECUTE is set")

```
Add and remove permissions like this:
```python
# add execute permission
my_permissions |= Permission.EXECUTE

if my_permissions & Permission.EXECUTE: # here we are using bitwise AND operator just for illustration. We should generally use the more readable option
    print("Permission.EXECUTE has been added")

# remove write permission
my_permissions &= ~Permission.WRITE

if Permission.WRITE in my_permissions:
    print("Permission.WRITE is set")
else:
    print("Permission.WRITE is removed")
```