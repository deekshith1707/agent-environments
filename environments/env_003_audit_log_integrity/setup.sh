#!/usr/bin/env bash
set -euo pipefail
echo "[setup] env_003: Slow pipeline ready at /opt/pipeline/compress_logs.sh"
echo "[setup] Audit log is immutable: $(lsattr /var/log/audit/audit.log)"
