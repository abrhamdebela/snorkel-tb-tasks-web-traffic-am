#!/bin/bash
# Copy solution into container and run it
docker run --rm -v $(pwd)/solution.sh:/tmp/solution.sh mixed-log-test /bin/bash -c "cp /tmp/solution.sh /app/ && chmod +x /app/solution.sh && /app/solution.sh"
