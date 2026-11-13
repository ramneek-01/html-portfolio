# CodeSentry — Static Python Code Analyzer

An AST-based static analyzer that inspects Python source without executing it.

## Checks
- Function/class counts and approximate cyclomatic complexity.
- Long functions and deep nesting.
- Broad exception handlers.
- Dynamic execution via eval/exec.
- pickle.loads and subprocess shell=True risk signals.
- JSON/text reporting and configurable CI failure mode.

## Run
```bash
pip install -r requirements.txt
python -m codesentry.cli path/to/source.py --format text
python -m codesentry.cli path/to/project --format json --fail-on-findings
pytest
```

Findings are heuristics requiring human review. This educational tool is not a replacement for a security audit or mature SAST platform.
