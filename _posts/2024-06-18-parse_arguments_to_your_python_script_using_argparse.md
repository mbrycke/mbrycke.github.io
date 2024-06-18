---
title: Parse arguments to your python script using argparse
date: 2024-06-18
categories: [programming, python, argparse]
tags: [python, argparse, subparsers]
---
    
We will look at a couple of examples to illustrate how to parse arguments to your Python script using the `argparse` module.


## The structure of the Python script

Notice that we read the arguments from `sys.argv` and then parse them using `argparse`.
The argparse module can read the arguments without `sys.argv` but it is a good practice to separate the argument parsing from the rest of the script.

```python
import argparse
import sys

def parse_arguments(args):
    parser = argparse.ArgumentParser(description='Description of your script')
    parser.add_argument('arg1', type=str, help='Description of arg1') # these are positional arguments and are required
    parser.add_argument('arg2', type=int, help='Description of arg2') # these are positional arguments and are required
    parser.add_argument('--arg3', action='store_true', help='Description of arg3') # store_true means that the argument is a boolean and will be True if the argument is present, i.e. --arg3 without a value
    parser.add_argument('--arg4', type=str, help='Description of arg4') # named arguments
    parser.add_argument('--arg5', type=str, default='default_value', help='Description of arg5') # named argument with default value
    parser.add_argument('--arg6', type=str, required=True, help='Description of arg6') # named argument that is required
    return parser.parse_args(args)

def main(args):
    args = parse_arguments(args)
    print(args)

if __name__== "__main__":
    main(sys.argv[1:])

```

To run this script we must give the two positional arguments and the explicitly required named argument `--arg6`. The other named arguments are optional.

```shell
python my_script.py arg1_value 42 --arg6 required_value
```

## Subparsers

Just like when e.g. using `git pull --rebase` where `pull` is a subcommand of `git`, you can use subparsers in argparse to have different commands in your script. Here is an example:


```python
import argparse
import sys


def parse_args(args):

    # Create the top-level parser
    parser = argparse.ArgumentParser(prog='math_tool')
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    # Create the parser for the "add" command
    parser_add = subparsers.add_parser('add', help='add help')
    parser_add.add_argument('numbers', type=int, nargs='+', help='List of numbers to add')

    # Create the parser for the "multiply" command
    parser_multiply = subparsers.add_parser('multiply', help='multiply help')
    parser_multiply.add_argument('numbers', type=int, nargs='+', help='List of numbers to multiply')

    # Create a parser for reading text
    parser_text = subparsers.add_parser('text', help='text help')
    parser_text.add_argument('text', type=str, help='Text to print')

    # Parse the arguments
    args = parser.parse_args()
    return args

# Implement the functionality based on the sub-command
def main(args):
    args=parse_args(args)
    if args.command == 'add':
        result = sum(args.numbers)
        print(f"The sum is: {result}")
    elif args.command == 'multiply':
        import math
        result = math.prod(args.numbers)
        print(f"The product is: {result}")
    elif args.command == 'text':
        print("This text was provided:", args.text)
    else:
        print("Invalid command")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
```

Example usage of the script:

```shell
python my_script.py add 1 2 3 4
# The sum is: 10

python my_script.py multiply 1 2 3 4
# The product is: 24

python my_script.py text "Hello world"
# This text was provided: Hello world
```