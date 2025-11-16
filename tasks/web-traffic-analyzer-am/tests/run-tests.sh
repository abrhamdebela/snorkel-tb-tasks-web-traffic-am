#!/usr/bin/env bash
set -euo pipefail

# Ensure tmp dir exists *inside /tests* (for test_outputs.py)
mkdir -p /tests/tmp

# 1) Run the solution from /workspace so "dataset/access.log" resolves correctly
cd /workspace
bash oracle/solution.sh > /tests/tmp/output.txt

# 2) Now run pytest from /tests so TB sees a normal pytest run
cd /tests
pytest --disable-warnings --maxfail=1 -rA
