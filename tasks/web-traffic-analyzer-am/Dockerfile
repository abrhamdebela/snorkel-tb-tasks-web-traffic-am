FROM python:3.10-slim

# Tools Terminal-Bench expects
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    tmux \
    asciinema \
 && rm -rf /var/lib/apt/lists/*

# Make sure all paths TB might use exist:
# - /tmp and /tests (normal Unix paths)
# - '\tmp' and '\tests' (weird Windows-style paths as literal names)
RUN mkdir -p /tmp /tests '\tmp' '\tests'

WORKDIR /workspace

# Copy task files into the container
COPY . .

# Install Python deps and make scripts executable,
# and COPY THE TEST RUNNER TO /tests/run-tests.sh (this is the key fix)
RUN pip install --no-cache-dir python-dateutil pytest \
 && chmod +x /workspace/oracle/solution.sh /workspace/tests/run-tests.sh \
 # copy ALL tests (including test_outputs.py) into /tests
 && cp -r /workspace/tests/. /tests \
 # make sure the test runner in /tests is executable
 && chmod +x /tests/run-tests.sh


CMD ["bash"]
