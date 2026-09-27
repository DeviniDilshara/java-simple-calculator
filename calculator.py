#!/usr/bin/env python3
"""
Simple CLI Calculator
Version: 1.0.0
Supports: addition, subtraction, multiplication, division, power, square root
"""

import math
import sys

VERSION = "1.0.0"


def add(a, b):
    return a + b


def subtract(a, b):
    # BUG (found in testing, see TC005): operands are swapped, giving b - a
    # instead of a - b.
    return b - a


def multiply(a, b):
    return a * b


def divide(a, b):
    # BUG (found in testing, see TC007): no guard for division by zero.
    # This raises an unhandled ZeroDivisionError and crashes the program.
    return a / b


def power(a, b):
    return a ** b


def square_root(a):
    return math.sqrt(a)


OPERATIONS = {
    "1": ("Add", add, 2),
    "2": ("Subtract", subtract, 2),
    "3": ("Multiply", multiply, 2),
    "4": ("Divide", divide, 2),
    "5": ("Power", power, 2),
    "6": ("Square Root", square_root, 1),
}


def menu():
    print(f"\n=== Simple Calculator v{VERSION} ===")
    for key, (name, _, _) in OPERATIONS.items():
        print(f"{key}. {name}")
    print("0. Exit")


def run():
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice not in OPERATIONS:
            print("Invalid option, try again.")
            continue

        name, func, arity = OPERATIONS[choice]
        try:
            if arity == 2:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                result = func(a, b)
            else:
                a = float(input("Enter number: "))
                result = func(a)
            print(f"Result: {result}")
        except ValueError:
            print("Error: please enter valid numbers.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print(VERSION)
    else:
        run()
