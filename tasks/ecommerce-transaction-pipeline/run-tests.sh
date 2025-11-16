#!/bin/bash

# Hint from Snorkel
# Script used to execute and validate the end-to-end evaluation of the task.

# Install curl if not available
apt-get update > /dev/null 2>&1
apt-get install -y curl > /dev/null 2>&1

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Create a virtual environment for test dependencies
uv venv /tmp/test-env

# Activate the virtual environment
source /tmp/test-env/bin/activate

# Install pytest and required test dependencies
uv pip install pytest==8.4.1 pandas==2.2.3 pyarrow==18.1.0

# Set test directory
export TEST_DIR=/tests

# Run tests
pytest $TEST_DIR/test_outputs.py -rA