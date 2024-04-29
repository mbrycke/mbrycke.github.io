---
title: Generator expression and Next() in Python
date: 2024-04-29
categories: [Python, generator, next()]
tags: [generators, next()]
---
    

A common scenario is to have a list of objects and we want to select a specific object.

E.g. 
```python

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

persons = [Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)]

```
Now imagine we only got the persons list and we want to select the person with the name 'Bob'. We could do this with a for loop:

```python

for person in persons:
    if person.name == 'Bob':
        print(person.name, person.age)
        target_person = person
        break
else:
    print('Person not found')
    target_person = None

```

However, using a generator expression and the next() function might be a more elegant way to do this:

```python

person = next((person for person in persons if person.name == 'Bob'), None)
```
The `next()` function will return the first item in the generator expression that matches the condition, i.e. the loop will break. If no item is found, it will return the default value, in this case `None`.

Remember the `next()` function syntax:
```python
next(iterator, default)
```
