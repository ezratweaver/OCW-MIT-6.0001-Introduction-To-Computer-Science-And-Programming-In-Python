"""Finger exercise: Implement a function that meets the specification
below. Use a try-except block. Hint: before starting to code, you
might want to type something like 1 + 'a' into the shell to see what
kind of exception is raised."""


def sum_digits(s):
    """Assumes s is a string
    Returns the sum of the decimal digits in s
    For example, if s is 'a2b3c' it returns 5"""
    total = 0
    for char in s:
        try:
            num = int(char)
        except ValueError:
            continue
        total += num
    return total


print(sum_digits("a2b3c"))
