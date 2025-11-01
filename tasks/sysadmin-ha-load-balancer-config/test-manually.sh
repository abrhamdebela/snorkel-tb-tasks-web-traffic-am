#!/bin/bash
# Manual testing script for sysadmin-ha-load-balancer-config task
set -e

TASK_DIR="/mnt/c/Users/david/snorkel-ai/snorkel-tb-tasks/tasks/sysadmin-ha-load-balancer-config"
PROJECT_NAME="sysadmin-ha-load-balancer-config-manual-test"

echo "=========================================="
echo "Manual Task Testing Script"
echo "=========================================="

# Get the client container name
CONTAINER_NAME=$(docker ps --filter "name=${PROJECT_NAME}" --filter "ancestor=tb__sysadmin-ha-load-balancer-config__client" --format "{{.Names}}" | head -1)

if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: Could not find client container"
    exit 1
fi

echo "Found container: $CONTAINER_NAME"

# Copy solution and test files to container
echo "Copying files to container..."
docker cp "$TASK_DIR/solution.sh" $CONTAINER_NAME:/tmp/solution.sh
docker cp "$TASK_DIR/tests" $CONTAINER_NAME:/tmp/tests
docker cp "$TASK_DIR/run-tests.sh" $CONTAINER_NAME:/tmp/run-tests.sh

# Run the solution
echo ""
echo "=========================================="
echo "Running solution.sh..."
echo "=========================================="
docker exec $CONTAINER_NAME bash /tmp/solution.sh

# Run the tests
echo ""
echo "=========================================="
echo "Running tests..."
echo "=========================================="
docker exec -e TEST_DIR=/tmp/tests $CONTAINER_NAME bash /tmp/run-tests.sh

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
echo "To cleanup: docker compose -p $PROJECT_NAME -f $TASK_DIR/docker-compose.yaml down"
