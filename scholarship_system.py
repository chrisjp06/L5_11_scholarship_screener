"""Scholarship screening system for evaluating applicant eligibility."""

import ast
import json
import operator
from typing import Any

DEFAULT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800_000
CUTOFF = 85

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate_merit_score(
    gpa: float, credit_count: int, formula: str
) -> float:
    """Evaluate a formula containing GPA, credits, numbers, and arithmetic."""
    try:
        expression = ast.parse(formula, mode="eval").body
    except SyntaxError as error:
        raise ValueError("Invalid merit formula syntax.") from error

    def evaluate(node: ast.AST) -> float:
        """Evaluate an allowlisted arithmetic expression recursively."""
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
        ):
            return float(node.value)

        if isinstance(node, ast.Name):
            variables = {"gpa": gpa, "credits": credit_count}
            if node.id not in variables:
                raise ValueError(f"Unsupported variable: {node.id}")
            return float(variables[node.id])

        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in _BINARY_OPERATORS
        ):
            left_value = evaluate(node.left)
            right_value = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right_value) > 10:
                raise ValueError("Exponent magnitude must not exceed 10.")

            return float(
                _BINARY_OPERATORS[type(node.op)](left_value, right_value)
            )

        if (
            isinstance(node, ast.UnaryOp)
            and type(node.op) in _UNARY_OPERATORS
        ):
            return float(
                _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
            )

        raise ValueError("Formula contains an unsupported expression.")

    try:
        return evaluate(expression)
    except (ArithmeticError, OverflowError) as error:
        raise ValueError("Merit formula could not be evaluated.") from error


def evaluate_applicant(
    student_id: str,
    test_scores: dict[str, Any],
    formula: str = DEFAULT_FORMULA,
    logs: list[str] | None = None,
    applicant_results: dict[str, dict[str, float | bool]] | None = None,
) -> bool:
    """Evaluate an applicant and store their eligibility result."""
    if logs is None:
        logs = []
    if applicant_results is None:
        applicant_results = {}

    gpa = float(test_scores["gpa"])
    credit_count = int(test_scores.get("credits", 0))
    income = float(test_scores.get("income", 0))

    if not 0 <= gpa <= 10:
        raise ValueError("GPA must be between 0 and 10.")
    if credit_count < 0:
        raise ValueError("Credits cannot be negative.")
    if income < 0:
        raise ValueError("Income cannot be negative.")

    score = calculate_merit_score(gpa, credit_count, formula)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    applicant_results[student_id] = {
        "score": score,
        "eligible": eligible,
    }
    logs.append(f"{student_id} scored {score}")

    return eligible


def change_formula(new_formula: str) -> str:
    """Validate a new merit formula before accepting it."""
    calculate_merit_score(1.0, 1, new_formula)
    return new_formula


def persist_results(
    applicant_results: dict[str, dict[str, float | bool]],
    file_name: str = "scholarships.json",
) -> None:
    """Save applicant results to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as output_file:
        json.dump(applicant_results, output_file, indent=2)


def load_results(
    file_name: str = "scholarships.json",
) -> dict[str, dict[str, float | bool]]:
    """Load applicant results from JSON, or return empty results if absent."""
    try:
        with open(file_name, "r", encoding="utf-8") as input_file:
            loaded_results = json.load(input_file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as error:
        raise ValueError(
            "The scholarship results file contains invalid JSON."
        ) from error

    if not isinstance(loaded_results, dict):
        raise ValueError(
            "The scholarship results file must contain a JSON object."
        )

    return loaded_results


def print_shortlist(
    applicant_results: dict[str, dict[str, float | bool]],
) -> None:
    """Print applicants who meet the scholarship cutoff."""
    print("Shortlisted applicants:")

    for student_id, applicant in applicant_results.items():
        if applicant["eligible"]:
            print(f"  {student_id} score = {applicant['score']}")


def main() -> None:
    """Run the scholarship screener."""
    applicant_results: dict[str, dict[str, float | bool]] = {}
    logs: list[str] = []
    formula = DEFAULT_FORMULA

    applicants = [
        ("U001", {"gpa": 9.1, "credits": 4, "income": 450_000}),
        ("U002", {"gpa": 7.2, "credits": 1, "income": 300_000}),
        ("U003", {"gpa": 12.5, "credits": -3, "income": -1}),
        ("U004", {"gpa": 6.5}),
    ]

    for student_id, test_scores in applicants:
        try:
            evaluate_applicant(
                student_id, test_scores, formula, logs, applicant_results
            )
        except ValueError as error:
            logs.append(f"{student_id} rejected: {error}")
            print(f"Skipping {student_id}: {error}")

    entered_formula = input(
        "Merit formula (Enter to keep default): "
    ).strip()

    if entered_formula:
        try:
            formula = change_formula(entered_formula)
        except ValueError as error:
            print(f"Invalid formula; using default. Reason: {error}")

    try:
        evaluate_applicant(
            "U005",
            {"gpa": 8.4, "credits": 3, "income": 600_000},
            formula,
            logs,
            applicant_results,
        )
    except ValueError as error:
        print(f"Skipping U005: {error}")

    persist_results(applicant_results)
    saved_results = load_results()
    print_shortlist(saved_results)


if __name__ == "__main__":
    main()
