# Lab 5 – Reflection

Static code analysis helped me identify security vulnerabilities, coding errors, and style violations in the scholarship screening system.

The original program contained several issues, including the use of `eval()`, mutable default arguments, global variables, unused imports, and improper exception handling.

The most important security improvement was replacing `eval()` with a restricted AST-based evaluator. This allows arithmetic expressions while preventing arbitrary code execution.

Other improvements included adding input validation, using specific exceptions, handling files with context managers, removing unused imports, and following Python naming and formatting conventions.

The three static analysis tools provided different benefits:

- **Pylint** identified code quality, maintainability, and naming issues.
- **Bandit** identified potential security vulnerabilities.
- **Flake8** identified style and formatting violations.

After applying the fixes, the program achieved a Pylint score of 10/10, Bandit reported no issues, and Flake8 reported no violations.

This lab demonstrated that static analysis tools can improve code security, readability, maintainability, and reliability before software is deployed.