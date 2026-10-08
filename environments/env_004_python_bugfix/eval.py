#!/usr/bin/env python3 -I
"""
Deterministic grader for env_004_python_bugfix.

Checks:
  1. All pytest tests pass (including new ones added by agent).
  2. At least 2 new test functions were added to test_aggregator.py.
  3. Existing test functions are still present (not deleted/skipped).
  4. Public signature of summarise_records unchanged.
  5. No new packages installed (only stdlib + pytest).
"""
import subprocess
import sys
import os
import ast

PASS, FAIL = 0, 1
results: list[str] = []
failed = False

ORIGINAL_TESTS = [
    "test_basic_summary",
    "test_single_record",
    "test_empty_records",
]
NEW_REQUIRED_TESTS = [
    "test_zero_count_records",
    "test_negative_value_records",
]


def check(condition: bool, message: str) -> None:
    global failed
    status = "PASS" if condition else "FAIL"
    if not condition:
        failed = True
    results.append(f"  [{status}] {message}")


def run(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=60, cwd=cwd)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


print("\n=== env_004 Grader ===\n")

# 1. Pytest passes
print("Check 1: All pytest tests pass")
rc, out = run(["python3", "-m", "pytest", "tests/", "-v", "--tb=short"],
              cwd="/opt/dataproc")
check(rc == 0, f"pytest exit code 0 (got {rc})\n{out[-2000:]}")

# 2. New test functions added
print("Check 2: New test functions present in test_aggregator.py")
test_file = "/opt/dataproc/tests/test_aggregator.py"
check(os.path.isfile(test_file), f"{test_file} exists")
if os.path.isfile(test_file):
    with open(test_file) as f:
        source = f.read()
    try:
        tree = ast.parse(source)
        fn_names = {n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)}
        summarise = next(
            (n for n in ast.walk(tree)
             if isinstance(n, ast.FunctionDef) and n.name == "summarise_records"),
            None,
        )
    except SyntaxError as e:
        fn_names = set()
        summarise = None
        check(False, f"test_aggregator.py has syntax error: {e}")

    new_count = sum(1 for name in fn_names
                    if name.startswith("test_") and name not in ORIGINAL_TESTS)
    check(new_count >= 2,
          f"At least 2 new test functions added (found {new_count})")

    for req in NEW_REQUIRED_TESTS:
        check(req in fn_names, f"Required test '{req}' is present")

# 3. Original tests not removed
print("Check 3: Original tests not removed or skipped")
if os.path.isfile(test_file):
    for name in ORIGINAL_TESTS:
        check(name in fn_names if "fn_names" in dir() else False,
              f"Original test '{name}' still present")

# 4. Public signature of summarise_records
print("Check 4: summarise_records signature unchanged")
agg_file = "/opt/dataproc/dataproc/aggregator.py"
check(os.path.isfile(agg_file), f"{agg_file} exists")
if os.path.isfile(agg_file):
    with open(agg_file) as f:
        agg_source = f.read()
    try:
        agg_tree = ast.parse(agg_source)
        summarise = next(
            (n for n in ast.walk(agg_tree)
             if isinstance(n, ast.FunctionDef) and n.name == "summarise_records"),
            None,
        )
        signature_ok = summarise is not None and [
            arg.arg for arg in summarise.args.args
        ] == ["records"] and summarise.args.vararg is None and summarise.args.kwarg is None
    except SyntaxError:
        signature_ok = False
    check(signature_ok, "summarise_records public signature remains (records)")

# Summary
print("\n--- Results ---")
for r in results:
    print(r)

if failed:
    print("\nVERDICT: FAIL")
    sys.exit(FAIL)
else:
    print("\nVERDICT: PASS")
    sys.exit(PASS)
