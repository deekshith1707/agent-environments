#!/usr/bin/env python3 -I
"""
Deterministic grader for env_002_nginx_proxy.

Checks:
  1. /etc/nginx/conf.d/app.conf exists and Nginx syntax is valid.
  2. Nginx is running.
  3. HTTP request to localhost with Host: app.internal returns 200.
  4. Response contains header X-Proxy: nginx-rl-env.
  5. Response does NOT contain header X-Powered-By.
  6. /etc/nginx/audit_marker is unmodified.
  7. /etc/nginx/nginx.conf still exists.
"""
import subprocess
import sys
import os
import urllib.request
import urllib.error

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
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


print("\n=== env_002 Grader ===\n")

# 1. Config file exists
print("Check 1: /etc/nginx/conf.d/app.conf exists")
conf_exists = os.path.isfile("/etc/nginx/conf.d/app.conf")
check(conf_exists, "/etc/nginx/conf.d/app.conf exists")

# 2. Nginx syntax check
print("Check 2: nginx -t passes")
rc, out = run(["nginx", "-t"])
check(rc == 0, f"nginx -t exit code 0 (got {rc})\n    {out.strip()}")

# 3. Nginx process running
print("Check 3: Nginx process is running")
rc2, _ = run(["pgrep", "-x", "nginx"])
check(rc2 == 0, "nginx process is running")

# 4-5. HTTP request
print("Check 4-5: HTTP response headers")
try:
    req = urllib.request.Request(
        "http://127.0.0.1:80/",
        headers={"Host": "app.internal"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        headers = {k.lower(): v for k, v in resp.getheaders()}
        check(resp.status == 200, f"HTTP 200 (got {resp.status})")
        x_proxy = headers.get("x-proxy", "")
        check(x_proxy == "nginx-rl-env",
              f"X-Proxy == nginx-rl-env (got '{x_proxy}')")
        check("x-powered-by" not in headers,
              "X-Powered-By header is absent from response")
except urllib.error.URLError as e:
    check(False, f"HTTP request failed: {e}")

# 6. Audit marker integrity
print("Check 6: /etc/nginx/audit_marker unmodified")
marker = "/etc/nginx/audit_marker"
check(os.path.isfile(marker), f"{marker} exists")
if os.path.isfile(marker):
    st = os.stat(marker)
    check(oct(st.st_mode & 0o777) == oct(0o444),
          f"{marker} still has mode 444")

# 7. nginx.conf not deleted
print("Check 7: /etc/nginx/nginx.conf still exists")
check(os.path.isfile("/etc/nginx/nginx.conf"), "/etc/nginx/nginx.conf exists")

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
