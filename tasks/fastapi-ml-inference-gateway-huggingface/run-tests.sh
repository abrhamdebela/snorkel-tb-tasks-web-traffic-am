#!/bin/bash

# Install curl
apt-get update
apt-get install -y curl

curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh

source $HOME/.local/bin/env

# Check if we're in a valid working directory
if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    exit 1
fi

# Install test dependencies and application dependencies needed by tests
uv venv .tbench-testing
source .tbench-testing/bin/activate

uv pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-asyncio==0.24.0 \
    requests==2.32.3 \
    aiohttp==3.11.7 \
    pandas==2.2.3 \
    aiosqlite==0.20.0 \
    typer==0.12.5 \
    fastapi==0.115.5 \
    uvicorn[standard]==0.32.1 \
    torch==2.5.1 \
    transformers==4.46.3 \
    numpy==2.1.3

# Run the tests
pytest $TEST_DIR/test_outputs.py -rA -v
