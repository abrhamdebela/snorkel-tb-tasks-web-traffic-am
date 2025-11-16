#!/usr/bin/env bash
set -euo pipefail

# TB sends: bash \tests\run-tests.sh
# Bash in the container interprets that as 'bash testrun-tests.sh' in /workspace.
# This wrapper then forwards to the real tests TB copied to /tests.
bash /tests/run-tests.sh
