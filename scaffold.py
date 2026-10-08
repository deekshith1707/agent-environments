#!/usr/bin/env python3
"""
scaffold.py — Generate a new RL environment skeleton instantly.

Usage:
    python3 scaffold.py --id 006 --name "cron_job_setup" --category system_admin
    python3 scaffold.py --id 007 --name "docker_firewall" --category safety_boundary

This creates:
  environments/env_006_cron_job_setup/
    ├── prompt.md
    ├── Dockerfile
    ├── setup.sh
    └── eval.py

with TODO markers where task-specific content belongs.
"""
import argparse
import json
import os
import re
import sys
import textwrap

CATEGORIES = [
    "system_admin",
    "safety_boundary",
    "refactoring",
    "state_verification",
    "network_config",
]

PROMPT_TEMPLATE = """\
# Task: {title}

## Objective
<!-- TODO: Describe what the agent must accomplish in 2-3 sentences. -->

## Instructions
1. <!-- TODO: Step 1 -->
2. <!-- TODO: Step 2 -->
3. <!-- TODO: Step 3 -->

## Constraints
- Do **not** modify `<!-- TODO: protected file or resource -->`.
- <!-- TODO: Add further safety constraints. -->

## Hints
- <!-- TODO: Add one or two non-trivial hints. -->
"""

DOCKERFILE_TEMPLATE = """\
FROM ubuntu:22.04

# TODO: Install required packages
RUN apt-get update -qq && apt-get install -y --no-install-recommends \\
    python3 \\
    && rm -rf /var/lib/apt/lists/*

# TODO: Seed the initial system state
# RUN ...

# TODO: Place the audit / protected file here
RUN echo "audit-seed-$(date -u +%s)" > /etc/env_{env_id}_audit && \\
    chmod 444 /etc/env_{env_id}_audit

WORKDIR /root
CMD ["/bin/bash"]
"""

SETUP_TEMPLATE = """\
#!/usr/bin/env bash
# setup.sh — dynamic seeding that runs inside the container before the agent starts.
set -euo pipefail
echo "[setup] env_{env_id} ready."
# TODO: Add any runtime seeding steps (e.g., generating random data).
"""

EVAL_TEMPLATE = """\
#!/usr/bin/env python3 -I
\"\"\"
Deterministic grader for env_{env_id}_{name}.

Exit codes:
  0 — PASS
  1 — FAIL
\"\"\"
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
    results.append(f"  [{{status}}] {{message}}")


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


print("\\n=== env_{env_id} Grader ===\\n")

# ── Check 1: TODO ─────────────────────────────────────────────────────────────
print("Check 1: TODO — describe what you are checking")
# check(os.path.isfile("/path/to/expected/file"), "expected file exists")

# ── Check 2: TODO ─────────────────────────────────────────────────────────────
print("Check 2: Audit file unmodified")
audit = "/etc/env_{env_id}_audit"
check(os.path.isfile(audit), f"{{audit}} exists")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\\n--- Results ---")
for r in results:
    print(r)

if failed:
    print("\\nVERDICT: FAIL")
    sys.exit(FAIL)
else:
    print("\\nVERDICT: PASS")
    sys.exit(PASS)
"""

SCENARIO_TEMPLATE = {
    "id": "env_{env_id}_{name}",
    "category": "{category}",
    "title": "{title}",
    "version": 1,
    "timeout_seconds": 120,
    "task": "TODO: Describe the measurable task.",
    "constraints": ["TODO: Add a safety constraint."],
    "reward": {"pass": 1, "fail": 0},
    "artifacts": ["TODO: Add inspected paths."]
}


def slugify(text: str) -> str:
    return text.lower().replace(" ", "_").replace("-", "_")


def title_case(slug: str) -> str:
    return slug.replace("_", " ").title()


def create_env(env_id: str, name: str, category: str) -> str:
    slug = slugify(name)
    if not re.fullmatch(r"[a-z0-9_]+", slug):
        raise ValueError("name must contain only letters, numbers, spaces, or underscores")
    if not re.fullmatch(r"\d{3}", env_id):
        raise ValueError("--id must be exactly three digits")
    dir_name = f"env_{env_id}_{slug}"
    env_dir = os.path.join("environments", dir_name)

    if os.path.exists(env_dir):
        print(f"[scaffold] Directory '{env_dir}' already exists — aborting.")
        sys.exit(1)

    os.makedirs(env_dir, exist_ok=True)

    ctx = {
        "env_id": env_id,
        "name": slug,
        "title": title_case(slug),
        "category": category,
    }

    files = {
        "prompt.md": PROMPT_TEMPLATE.format(**ctx),
        "Dockerfile": DOCKERFILE_TEMPLATE.format(**ctx),
        "setup.sh": SETUP_TEMPLATE.format(**ctx),
        "eval.py": EVAL_TEMPLATE.format(**ctx),
        "scenario.json": json.dumps(
            {key: value.format(**ctx) if isinstance(value, str) else value
             for key, value in SCENARIO_TEMPLATE.items()},
            indent=2,
        ) + "\n",
    }

    for fname, content in files.items():
        fpath = os.path.join(env_dir, fname)
        with open(fpath, "w") as f:
            f.write(content)
        if fname in ("setup.sh", "eval.py"):
            os.chmod(fpath, 0o755)

    return env_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new RL environment skeleton.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""\
            Categories:
              {chr(10).join("  " + c for c in CATEGORIES)}

            Example:
              python3 scaffold.py --id 006 --name cron_job_setup --category system_admin
        """),
    )
    parser.add_argument("--id",       required=True, help="3-digit environment ID, e.g. 006")
    parser.add_argument("--name",     required=True, help="Short snake_case name, e.g. cron_job_setup")
    parser.add_argument("--category", required=True, choices=CATEGORIES, help="Task category")
    args = parser.parse_args()

    try:
        env_dir = create_env(args.id, args.name, args.category)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"[scaffold] Created: {env_dir}/")
    print(f"[scaffold] Files: prompt.md  Dockerfile  setup.sh  eval.py  scenario.json")
    print(f"[scaffold] Fill in the TODO markers and you're ready to test!")


if __name__ == "__main__":
    main()
