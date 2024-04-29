---
title: Generator expression and next() in Python
date: 2024-04-29
categories: [Python, generator, next()]
tags: [generators, next()]
---
    

A common scenario is to have a list of objects from which we want to select a specific object.

E.g. 
```python

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

persons = [Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)]

```
To select the person with the name 'Bob' we could use a for loop like this:

```python

for person in persons:
    if person.name == 'Bob':
        target_person = person
        break
else:
    print('Person not found')
    target_person = None

print(target_person.name, target_person.age)
```

However, using a generator expression and the next() function might be a more elegant way to do this:

```python

person = next((person for person in persons if person.name == 'Bob'), None)

print(person.name, person.age)
```
The `next()` function will return the first item in the generator expression that matches the condition, i.e. the loop will break. If no item is found, it will return the default value, in this case `None`.

Remember the `next()` function syntax:
```python
next(iterator, default)
```

Using list comprehension is also an option, but it will be less efficient since it will iterate over the entire list (list comprehension does not have a break statement):
```python
person = [person for person in persons if person.name == 'Bob'][0] # less efficient
```