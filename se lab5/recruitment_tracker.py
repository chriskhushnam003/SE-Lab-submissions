"""Recruitment tracker for managing applicant records and shortlists."""

import ast
import csv
import sqlite3

conn = sqlite3.connect(":memory:")


def initialise_database():
    """Create the applicants table if it does not already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            expected_salary INTEGER NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conn.commit()


def add_applicant(name, role, expected_salary, status="applied"):
    """Insert a new applicant record into the database."""
    if not name or not role:
        raise ValueError("Name and role cannot be empty.")
    if expected_salary < 0:
        raise ValueError("Expected salary cannot be negative.")

    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) "
        "VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def _evaluate_salary_expression(expression):
    """Safely evaluate a simple arithmetic expression.

    This is used to turn a salary cap such as "500000 + 150000" into a
    numeric limit.
    """
    if isinstance(expression, (int, float)):
        return int(expression)

    if not isinstance(expression, str):
        raise TypeError(
            "Salary rule must be a number or arithmetic expression."
        )

    parsed = ast.parse(expression.strip(), mode="eval")
    return _evaluate_ast_node(parsed.body)


def _evaluate_ast_node(node):
    """Recursively evaluate a restricted arithmetic AST."""
    if isinstance(node, ast.Constant):
        return int(node.value)
    if isinstance(node, ast.UnaryOp):
        value = _evaluate_ast_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
        raise ValueError("Unsupported unary operator in salary expression.")
    if isinstance(node, ast.BinOp):
        left = _evaluate_ast_node(node.left)
        right = _evaluate_ast_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        raise ValueError("Unsupported operator in salary expression.")
    raise ValueError("Unsupported salary expression.")


def shortlist(role, salary_rule):
    """Return all applicants for a role whose salary is within the cap."""
    limit = _evaluate_salary_expression(salary_rule)
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?",
        (role,),
    ).fetchall()

    shortlisted = [name for name, salary in rows if salary <= limit]
    return shortlisted or []


def update_status(applicant_id, status):
    """Update an applicant status.

    Returns True when the target applicant exists; otherwise False.
    """
    if not status:
        raise ValueError("Status cannot be empty.")

    cursor = conn.execute(
        "UPDATE applicants SET status = ? WHERE id = ?",
        (status, applicant_id),
    )
    conn.commit()
    return cursor.rowcount > 0


def export_report(path):
    """Export all applicant records as a CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["name", "role", "status"])
        for name, role, status in conn.execute(
            "SELECT name, role, status FROM applicants"
        ):
            writer.writerow([name, role, status])


def count_by_status(status):
    """Count applicants matching a specific status."""
    return conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?",
        (status,),
    ).fetchone()[0]


def main():
    """Run a basic demonstration of the applicant tracker."""
    initialise_database()
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
