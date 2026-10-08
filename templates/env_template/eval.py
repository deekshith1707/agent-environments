#!/usr/bin/env python3 -I
"""
Deterministic grader template.

Replace each TODO block with real assertions.
Exit 0 = PASS, Exit 1 = FAIL.
"""
import os
import sys
import subprocess

PASS, FAIL = 0, 1
results: list[str] = []
failed = False


def check(condition: bool, message: str) -> None:
    global failed
    status = "PASS" if condition else "FAIL"
    if not condition:
        failed = True
    results.append(f"  [{status}] {message}")


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


print("\n=== <ENV_NAME> Grader ===\n")

# ── Check 1: TODO ─────────────────────────────────────────────────────────────
print("Check 1: <describe>")
# check(os.path.isfile("/expected/path"), "expected file exists")

# ── Check N: Audit file unmodified ────────────────────────────────────────────
print("Check N: Audit file unmodified")
audit = "/etc/template_audit"
check(os.path.isfile(audit), f"{audit} still exists")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n--- Results ---")
for r in results:
    print(r)

if failed:
    print("\nVERDICT: FAIL")
    sys.exit(FAIL)
else:
    print("\nVERDICT: PASS")
    sys.exit(PASS)
