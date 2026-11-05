# Lab 5 – Static Code Analysis

## Issue Table

| Tool | Issue Identified | Severity / Type | Fix Applied |
|---|---|---|---|
| Pylint | Use of `eval()` | Security concern | Replaced with a restricted AST-based arithmetic evaluator |
| Pylint | Mutable default argument `logs=[]` | Code quality | Changed to `None` and initialized inside the function |
| Pylint | Unused imports (`math`, `sys`) | Code quality | Removed unused imports |
| Pylint | Missing module and function docstrings | Code quality | Added documentation strings |
| Pylint | Global variable modification | Code quality | Passed result dictionaries explicitly |
| Pylint | Bare `except` statement | Error handling | Used specific exception types |
| Pylint | Function naming convention violation | Style | Renamed `printShortlist()` to `print_shortlist()` |
| Bandit | B307 – Use of `eval()` | Medium severity | Replaced `eval()` with safe expression evaluation |
| Bandit | B110 – Try/except/pass | Low severity | Replaced silent exception handling with explicit handling |
| Flake8 | Unused imports | F401 | Removed unused imports |
| Flake8 | Incorrect blank lines | E302, E305 | Corrected spacing |
| Flake8 | Bare except | E722 | Replaced with specific exception handling |
| Flake8 | Comparison to `True` | E712 | Used direct Boolean condition |
| Flake8 | Lines exceeding 79 characters | E501 | Wrapped long lines |

## Final Results

- Pylint: 10/10
- Bandit: No issues identified
- Flake8: No issues reported