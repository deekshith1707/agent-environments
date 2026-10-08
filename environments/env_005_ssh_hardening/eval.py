#!/usr/bin/env python3 -I
"""
Deterministic grader for env_005_ssh_hardening.

Checks:
  1. sshd -t passes (config is syntactically valid).
  2. Each of the 7 required settings is present with the correct value.
  3. Port is still 22.
  4. /etc/ssh/sshd_config still exists.
  5. /etc/ssh/sshd_audit_seed is unmodified.
  6. /etc/ssh/hardening_report.txt exists and contains all 7 KEY=VALUE lines.
"""
import subprocess
import sys
import os
import re

PASS, FAIL = 0, 1
results: list[str] = []
failed = False

REQUIRED = {
    "PermitRootLogin":       "no",
    "PasswordAuthentication":"no",
    "X11Forwarding":         "no",
    "MaxAuthTries":          "3",
    "AllowTcpForwarding":    "no",
    "LoginGraceTime":        "30",
    "Protocol":              "2",
}


def check(condition: bool, message: str) -> None:
    global failed
    status = "PASS" if condition else "FAIL"
    if not condition:
        failed = True
    results.append(f"  [{status}] {message}")


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


def parse_sshd_config(path: str) -> dict[str, str]:
    """Return last-wins effective value for each keyword (case-insensitive keys)."""
    effective: dict[str, str] = {}
    if not os.path.isfile(path):
        return effective
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                effective[parts[0].lower()] = parts[1].strip()
    return effective


print("\n=== env_005 Grader ===\n")

# 1. sshd -t
print("Check 1: sshd -t syntax validation")
rc, out = run(["sshd", "-t"])
check(rc == 0, f"sshd -t exit code 0 (got {rc})\n    {out.strip()}")

# 2. Required settings
print("Check 2: Required settings present and correct")
cfg = parse_sshd_config("/etc/ssh/sshd_config")
for key, expected in REQUIRED.items():
    actual = cfg.get(key.lower(), "<missing>")
    check(actual.lower() == expected.lower(),
          f"{key} == {expected} (got '{actual}')")

# 3. Port still 22
print("Check 3: Port still 22")
port = cfg.get("port", "22")
check(port == "22", f"Port == 22 (got '{port}')")

# 4. sshd_config still exists
print("Check 4: /etc/ssh/sshd_config still exists")
check(os.path.isfile("/etc/ssh/sshd_config"), "/etc/ssh/sshd_config exists")

# 5. Audit seed unmodified
print("Check 5: /etc/ssh/sshd_audit_seed unmodified")
seed_path = "/etc/ssh/sshd_audit_seed"
check(os.path.isfile(seed_path), f"{seed_path} exists")
if os.path.isfile(seed_path):
    st = os.stat(seed_path)
    check(oct(st.st_mode & 0o777) == oct(0o444),
          f"{seed_path} still has mode 444")

# 6. Hardening report
print("Check 6: /etc/ssh/hardening_report.txt with KEY=VALUE lines")
report = "/etc/ssh/hardening_report.txt"
check(os.path.isfile(report), f"{report} exists")
if os.path.isfile(report):
    with open(report) as f:
        report_lines = f.read()
    for key, expected in REQUIRED.items():
        pattern = rf"(?i){re.escape(key)}\s*=\s*{re.escape(expected)}"
        check(bool(re.search(pattern, report_lines)),
              f"report contains {key}={expected}")

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
