# Agentic Environments

A learning project for building Docker-based benchmark environments that test
autonomous AI agents with deterministic pass/fail graders.

Included scenarios:

- Linux permissions hardening
- Nginx reverse-proxy configuration
- Audit-safe log optimization
- Python bug fixing
- SSH security hardening

Each environment contains a task prompt, Docker setup, scenario metadata, and
an executable evaluator. A scaffold generator and shared runner make it easy
to create and test additional environments.

## Quick start

```bash
python3 -m unittest discover -s tests -v
./run_all_evals.sh
./run_all_evals.sh env_001_linux_permissions --interactive
```
