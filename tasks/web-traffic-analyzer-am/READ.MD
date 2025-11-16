# Web Traffic Analyzer (web-traffic-analyzer-am)

This task asks an agent to implement a command-line tool that analyzes a web
server access log and produces a summary of traffic and anomalies.

## Input

A log file in Apache access.log format at:

`dataset/access.log`

## Required behavior

- Parse each log line and extract IP, timestamp, method, path, status code.
- Compute:
  - total requests
  - unique visitors
  - top 10 URLs
  - top 10 IPs
  - per-method counts
  - per-status-category counts (2xx, 3xx, 4xx, 5xx)
- Detect:
  - IPs with >100 requests in 60 seconds
  - bursts of >20 5xx errors in 60 seconds
- Print a human-readable report.

## Reference solution

See `solution.py`.
