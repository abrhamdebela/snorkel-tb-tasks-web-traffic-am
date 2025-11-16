#!/usr/bin/env bash
set -euo pipefail

# Directory this script lives in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the reference solution (Python script)
python /workspace/oracle/solution.py