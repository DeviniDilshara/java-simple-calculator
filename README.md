# Simple CLI Calculator

A basic command-line calculator written in Python 3, built as part of a
software-testing activity: implement → write test cases → test → find bugs →
fix → re-test → version-bump.

## Features
- Addition, Subtraction, Multiplication, Division
- Power (exponent)
- Square Root
- Simple numbered-menu CLI

## Usage
```bash
python3 calculator.py          # interactive menu
python3 calculator.py --version
```

## Requirements
Python 3.7+. No external dependencies.

## Testing
Test case scenarios, execution results, and bug status for each version are
tracked in `Calculator_Test_Cases.xlsx` (see the "Test Case Results" sheet).

## Version History
| Version | Date       | Notes |
|---------|------------|-------|
| 1.0.0   | 2026-09-27 | Initial implementation. |
| 2.0.0   | 2026-09-27 | Fixed subtraction operand order bug (TC005) and division-by-zero crash (TC007). Added input validation for square root of negative numbers. |

## License
MIT
