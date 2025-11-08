"""
Target module for bytecode patching demonstration.
This module will be compiled and then patched to intercept function calls.
"""


def calculate(x, y):
    """Main function that calls other functions."""
    result = add(x, y) + multiply(x, y)
    return result


def add(a, b):
    """Simple addition function."""
    return a + b


def multiply(a, b):
    """Simple multiplication function."""
    return a * b


def helper(value):
    """Helper function for testing."""
    return value * 2


def nested_calls(x):
    """Function with nested calls."""
    temp = helper(x)
    return add(temp, multiply(x, 3))


if __name__ == "__main__":
    print(f"calculate(3, 4) = {calculate(3, 4)}")
    print(f"nested_calls(5) = {nested_calls(5)}")