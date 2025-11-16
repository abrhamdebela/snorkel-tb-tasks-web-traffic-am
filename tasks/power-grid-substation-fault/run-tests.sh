#!/bin/bash





set -euo pipefail

# Check working directory
if [ "$PWD" = "/" ]; then
    echo "Error: WORKDIR is not set in Dockerfile" >&2
    exit 1
fi

# Ensure TEST_DIR variable is set
if [ -z "${TEST_DIR:-}" ]; then
    echo "TEST_DIR environment variable not set" >&2
    exit 1
fi

# Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..." >&2
    python3 -m pip install --no-cache-dir uv==0.7.13 >/dev/null
fi

# Create isolated environment for tests
VENV_PATH=".tbench-testing"
uv venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

# Install pytest
uv pip install pytest==8.4.1 >/dev/null

# Run all validation tests
uv run pytest "${TEST_DIR}/test_outputs.py" -rA
