import ast
import sys
from pathlib import Path
def violations(source):
    return [node.lineno for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.ExceptHandler)
            and len(node.body) == 1 and isinstance(node.body[0], ast.Pass)]
if __name__ == "__main__":
    findings = [(name, line) for name in sys.argv[1:]
                for line in violations(Path(name).read_text())]
    for name, line in findings:
        print(f"{name}:{line}: empty exception handler; propagate or handle the error")
    raise SystemExit(bool(findings))
