#!/usr/bin/env bash
# setup.sh — run inside the container before handing control to the agent
# (This is a no-op here because the Dockerfile already seeds state,
#  but the hook exists for dynamic/randomised seeding in CI pipelines.)
set -euo pipefail
echo "[setup] env_001 ready — /var/www/html is seeded with bad permissions."
