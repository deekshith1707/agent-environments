#!/usr/bin/env bash
set -euo pipefail

# Start upstream Node app
node /opt/app/server.js &
echo "[entrypoint] Node app started (pid $!)"

# Start Nginx in daemon mode so its PID file supports `nginx -s reload`.
nginx
echo "[entrypoint] Nginx started"

if [[ "$#" -gt 0 ]]; then
    exec "$@"
fi
exec /bin/bash
