# ci/pre-commit/technical_debt_tracker.py
import ast
import glob

DEBT_MARKERS = {
    "TODO": "P3",
    "FIXME": "P2",
    "HACK": "P1",
    "DEPRECATED": "P0"
}

def scan_for_debt():
    debt_report = {}
    for file in glob.glob("**/*.py", recursive=True):
        with open(file, "r") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                    comment = node.value.value
                    for marker, priority in DEBT_MARKERS.items():
                        if marker in comment:
                            debt_report.setdefault(file, []).append({
                                "line": node.lineno,
                                "marker": marker,
                                "priority": priority,
                                "comment": comment
                            })
    # Generate JIRA tickets
    for file, items in debt_report.items():
        for item in items:
            create_jira_issue(
                title=f"TechDebt: {item['marker']} in {file}",
                description=f"{item['comment']}\n\nFile: {file}:{item['line']}",
                priority=item["priority"]
            )