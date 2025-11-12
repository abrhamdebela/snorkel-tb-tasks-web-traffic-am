#!/bin/bash

# Hint from Snorkel
# Script used to execute and validate the end-to-end evaluation of the task.
# It coordinates running the agent within the defined environment,
# invokes test cases or success criteria checks, and produces structured output
# (e.g., logs or JSON summaries) that indicate task completion status.
# It must be deterministic, portable, and callable directly from the project root.

# Install curl
apt-get update
apt-get install -y curl

# Install uv
curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh

source $HOME/.local/bin/env

# Check if we're in a valid working directory
if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

# Use system Python with --system-site-packages to reuse packages already installed in Dockerfile
# This avoids re-downloading pandas, numpy, scipy which are already installed (saves ~30MB download)
uv venv .tbench-testing --system-site-packages
source .tbench-testing/bin/activate

# Install test dependencies (pytest and pytest-timeout)
# System packages (pandas, numpy, scipy) are already available via --system-site-packages
uv pip install pytest==8.4.1 pytest-timeout==2.3.1

# Install other dependencies if needed (remember, by default this is a different venv
# than your agent's)

# Run tests with per-test timeout (30 seconds per test to catch hanging tests faster)
# The overall test suite timeout is controlled by max_test_timeout_sec in task.yaml
uv run pytest $TEST_DIR/test_outputs.py -rA --timeout=30