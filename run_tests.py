#!/usr/bin/env python3
"""Runs the fixed set of test cases against calculator.py and prints JSON results."""
import json
import importlib
import math

import calculator
importlib.reload(calculator)

TEST_CASES = [
    ("TC001", "Add two positive numbers", "add", (5, 3), 8),
    ("TC002", "Add two negative numbers", "add", (-5, -3), -8),
    ("TC003", "Add with zero", "add", (0, 0), 0),
    ("TC004", "Multiply two positive numbers", "multiply", (6, 7), 42),
    ("TC005", "Subtract: a minus b (order matters)", "subtract", (10, 4), 6),
    ("TC006", "Multiply by zero", "multiply", (5, 0), 0),
    ("TC007", "Divide by zero (should not crash)", "divide", (10, 0), "ERROR_HANDLED"),
    ("TC008", "Divide two normal numbers", "divide", (10, 2), 5),
    ("TC009", "Power / exponent", "power", (2, 3), 8),
    ("TC010", "Square root of positive number", "square_root", (16,), 4),
    ("TC011", "Square root of negative number (should not crash)", "square_root", (-4,), "ERROR_HANDLED"),
    ("TC012", "Add decimal numbers", "add", (2.5, 1.5), 4.0),
]

results = []
for tc_id, desc, fn_name, args, expected in TEST_CASES:
    fn = getattr(calculator, fn_name)
    try:
        actual = fn(*args)
        if expected == "ERROR_HANDLED":
            # Passes only if the function returns a graceful error message
            # (a string) instead of raising or returning a bogus number.
            if isinstance(actual, str) and actual.lower().startswith("error"):
                status = "PASS"
            else:
                status = "FAIL"
            actual_display = actual
        else:
            status = "PASS" if actual == expected else "FAIL"
            actual_display = actual
    except Exception as e:
        if expected == "ERROR_HANDLED":
            status = "FAIL"  # crashed instead of failing gracefully
            actual_display = f"CRASH: {type(e).__name__}: {e}"
        else:
            status = "FAIL"
            actual_display = f"CRASH: {type(e).__name__}: {e}"
    results.append({
        "id": tc_id,
        "description": desc,
        "function": fn_name,
        "inputs": args,
        "expected": expected,
        "actual": actual_display,
        "status": status,
    })

print(json.dumps(results, indent=2, default=str))
