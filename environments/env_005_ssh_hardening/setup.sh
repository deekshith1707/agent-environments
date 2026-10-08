#!/usr/bin/env bash
set -euo pipefail
echo "[setup] env_005: Insecure sshd_config is at /etc/ssh/sshd_config"
echo "[setup] Current PermitRootLogin: $(grep PermitRootLogin /etc/ssh/sshd_config || echo 'not set')"
