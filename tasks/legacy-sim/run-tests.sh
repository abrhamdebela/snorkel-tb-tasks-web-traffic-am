#!/bin/bash

set -euo pipefail

apt-get update
apt-get install -y curl

UV_VERSION="0.7.13"
UV_INSTALL_SCRIPT="https://astral.sh/uv/${UV_VERSION}/install.sh"
UV_INSTALLER="$(mktemp)"

curl -LsSf "$UV_INSTALL_SCRIPT" -o "$UV_INSTALLER"

chmod +x "$UV_INSTALLER"
env UV_LINK_MODE=copy sh "$UV_INSTALLER"
rm -f "$UV_INSTALLER"

source "$HOME/.local/bin/env"

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

uv venv
uv pip install pytest==8.4.1

uv run pytest "$TEST_DIR/test_outputs.py" -rA
