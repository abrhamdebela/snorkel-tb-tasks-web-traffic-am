#!/bin/bash

# You can modify anything in this script. Just make sure it generates test output that
# is parsed by a parser (PytestParser by default).

set -euo pipefail

# Check if we're in a valid working directory
if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script." >&2
    exit 1
fi

if [ -z "${TEST_DIR:-}" ]; then
    echo "TEST_DIR environment variable is not set." >&2
    exit 1
fi

# Install curl if not available
if ! command -v curl >/dev/null 2>&1; then
    apt-get update && apt-get install -y curl
fi

# Install uv if not available
if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh
    source $HOME/.local/bin/env 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
fi

# Set up Python testing environment
VENV_PATH=".tbench-testing"
uv venv "$VENV_PATH"
. "$VENV_PATH/bin/activate"

# Install test dependencies
uv pip install pytest==8.4.1

# Run tests (solution.sh should have already been run by the oracle agent)
uv run pytest "${TEST_DIR}/test_outputs.py" -rA
