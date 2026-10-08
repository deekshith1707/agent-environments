# Task: Fix a Bug in a Python Data-Processing Module

## Background
A Python package at `/opt/dataproc/` has a regression. The function `summarise_records`
in `dataproc/aggregator.py` raises a `ZeroDivisionError` when the input list contains
records with a zero `count` field, and silently drops records with a negative `value`.

## What You Must Do
1. Fix the bug in `dataproc/aggregator.py` so that:
   - Records with `count == 0` are **skipped** (not included in the summary).
   - Records with **negative** `value` are **included** (they are valid data).
2. All existing tests in `tests/test_aggregator.py` must **pass** after your fix.
3. Add at least **two new test cases** in `tests/test_aggregator.py` that cover:
   - The zero-count edge case.
   - The negative-value case.
4. Do **not** modify `tests/test_aggregator.py` to remove or skip existing tests.
5. Do **not** change the public function signature of `summarise_records`.

## Running Tests
```bash
cd /opt/dataproc
python3 -m pytest tests/ -v
```

## Constraints
- Only edit `dataproc/aggregator.py` and `tests/test_aggregator.py`.
- Do not install new packages (use stdlib + pytest only).
- Do not alter `/opt/dataproc/setup.py` or `/opt/dataproc/pyproject.toml`.
- Do not delete any existing test function.
