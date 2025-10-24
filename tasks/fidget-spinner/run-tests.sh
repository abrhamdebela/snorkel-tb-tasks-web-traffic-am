#!/bin/bash

# Terminal-Bench test runner for fidget spinner task
# This script sets up the test environment and runs pytest

set -euo pipefail

UV_VERSION="0.7.13"
UV_INSTALL_SCRIPT="https://astral.sh/uv/${UV_VERSION}/install.sh"
UV_INSTALLER="$(mktemp)"

# Download the uv installer script without relying on curl/wget availability.
python - "$UV_INSTALL_SCRIPT" "$UV_INSTALLER" <<'PY'
import sys
from pathlib import Path
from urllib.request import urlopen

url, destination = sys.argv[1], sys.argv[2]
with urlopen(url) as response:
    Path(destination).write_bytes(response.read())
PY

chmod +x "$UV_INSTALLER"
env UV_LINK_MODE=copy sh "$UV_INSTALLER"
rm -f "$UV_INSTALLER"

source "$HOME/.local/bin/env"

# Check if we're in a valid working directory
if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

uv init
uv add pytest==8.4.1

# Run the tests
uv run pytest "$TEST_DIR/test_outputs.py" -rA
