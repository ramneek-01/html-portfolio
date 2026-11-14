# CodeSentry — Python Static Analyzer

An AST-based analyzer that inspects Python source without executing it.

## Checks
- Function and class counts.
- Approximate cyclomatic complexity.
- Long functions and deep nesting.
- Broad exception handlers.
- Dynamic execution through `eval` and `exec`.
- `pickle.loads` and `subprocess` calls using `shell=True`.
- Text and JSON reports with configurable failure thresholds.

## Run
```bash
pip install -r requirements.txt
python -m codesentry.cli path/to/source.py --format text
python -m codesentry.cli path/to/project --format json --fail-on-findings
pytest
```

Findings are heuristic signals and need manual review. This tool is not a substitute for a security audit.
