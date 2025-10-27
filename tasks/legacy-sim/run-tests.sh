#!/bin/bash

set -euo pipefail

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --no-input --quiet pytest==8.4.1
python3 -m pytest "$TEST_DIR/test_outputs.py" -rA
