#!/bin/bash

set -euo pipefail

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    else
        python3 -m ensurepip --upgrade >/dev/null 2>&1 || true
        python3 -m pip install --no-input --quiet uv
    fi
fi

uv venv .tbench-testing
source .tbench-testing/bin/activate
pip install --no-input --quiet pytest==8.4.1
pytest "$TEST_DIR/test_outputs.py" -rA
