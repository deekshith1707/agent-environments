#!/usr/bin/env bash
# Build and grade environments without losing the agent's container state.
#
# Usage:
#   ./run_all_evals.sh                         # verify seeded states fail
#   ./run_all_evals.sh env_003 --interactive  # solve one environment, then grade it
#   ./run_all_evals.sh --interactive           # solve each environment in sequence
#
# In interactive mode the same named container is graded after the agent exits.
# This is important: starting a second container from the image would discard
# all changes made by the agent.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENVS_DIR="$SCRIPT_DIR/environments"
FILTER=""
INTERACTIVE=0
KEEP=0

for arg in "$@"; do
    case "$arg" in
        --interactive) INTERACTIVE=1 ;;
        --keep) KEEP=1 ;;
        --help|-h)
            sed -n '2,12p' "$0"
            exit 0
            ;;
        *) FILTER="$arg" ;;
    esac
done

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

run_env() {
    local env_path="$1"
    local env_name
    env_name="$(basename "$env_path")"
    local image_tag="rl-env-${env_name}:latest"
    local container_name="rl-env-${env_name}-run"

    echo ""
    echo "============================================================"
    echo "  ENV: $env_name"
    echo "============================================================"

    if ! docker build -q -t "$image_tag" "$env_path"; then
        echo "[build] FAILED"
        ((SKIP_COUNT++)) || true
        return
    fi

    docker rm -f "$container_name" >/dev/null 2>&1 || true
    local exit_code
    if [[ "$INTERACTIVE" -eq 1 ]]; then
        echo "[agent] Solve the task in the container, then exit."
        set +e
        # Keep PID 1 alive in the background, then attach only the agent shell.
        # When that shell exits, docker exec returns and grading can begin.
        docker run --name "$container_name" -d "$image_tag" \
            /bin/bash -lc 'while :; do sleep 3600; done' >/dev/null
        docker exec -it "$container_name" /bin/bash
        exit_code=$?
        set -e
        if [[ "$exit_code" -ne 0 ]]; then
            echo "[agent] container exited with code $exit_code"
            ((FAIL_COUNT++)) || true
            return
        fi
        docker cp "$env_path/eval.py" "$container_name:/root/eval.py"
        set +e
        docker exec "$container_name" python3 /root/eval.py
        exit_code=$?
        set -e
    else
        echo "[seeded] Grading initial state (expected to fail until an agent solves it)."
        set +e
        docker run --rm \
            -v "$env_path/eval.py:/root/eval.py:ro" \
            "$image_tag" python3 /root/eval.py
        exit_code=$?
        set -e
        if [[ "$exit_code" -eq 1 ]]; then
            echo "[seeded] correctly failed"
            ((PASS_COUNT++)) || true
        else
            echo "[seeded] expected grader exit code 1, got $exit_code"
            ((FAIL_COUNT++)) || true
        fi
        return
    fi

    if [[ "$exit_code" -eq 0 ]]; then
        echo "[grade] PASS $env_name"
        ((PASS_COUNT++)) || true
    else
        echo "[grade] FAIL $env_name (exit code $exit_code)"
        ((FAIL_COUNT++)) || true
    fi

    if [[ "$KEEP" -eq 0 ]]; then
        docker rm -f "$container_name" >/dev/null
    else
        echo "[keep] container retained as $container_name"
    fi
}

found=0
for env_path in "$ENVS_DIR"/env_*/; do
    [[ -d "$env_path" ]] || continue
    env_name="$(basename "$env_path")"
    if [[ -n "$FILTER" && "$env_name" != *"$FILTER"* ]]; then
        continue
    fi
    found=1
    run_env "$env_path"
done

if [[ "$found" -eq 0 ]]; then
    echo "No environment matched: ${FILTER:-<none>}" >&2
    exit 2
fi

echo ""
echo "RESULTS: PASS=$PASS_COUNT FAIL=$FAIL_COUNT SKIP=$SKIP_COUNT"
[[ "$FAIL_COUNT" -eq 0 && "$SKIP_COUNT" -eq 0 ]]
