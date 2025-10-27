#!/bin/bash

set -e

cat > /app/analyze_logs.py << 'EOF'
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path

def parse_timestamp(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")

def parse_log_file(filepath):
    errors = []
    log_name = Path(filepath).stem  # 'api', 'database', or 'cache'

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Match timestamp and log level
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ERROR|CRITICAL) (.+)', line)
            if match:
                timestamp_str, level, message = match.groups()
                errors.append({
                    'timestamp': parse_timestamp(timestamp_str),
                    'timestamp_str': timestamp_str,
                    'level': level,
                    'message': message,
                    'source': log_name
                })

    return errors

def find_correlations(all_errors, window_seconds=5):
    sorted_errors = sorted(all_errors, key=lambda x: x['timestamp'])

    correlated_groups = []
    used_indices = set()

    for i, error in enumerate(sorted_errors):
        if i in used_indices:
            continue

        group = [error]
        group_sources = {error['source']}
        group_indices = {i}

        for j in range(i + 1, len(sorted_errors)):
            if j in used_indices:
                continue

            time_diff = (sorted_errors[j]['timestamp'] - error['timestamp']).total_seconds()

            if time_diff <= window_seconds:
                # Only add if from different source
                if sorted_errors[j]['source'] not in group_sources:
                    group.append(sorted_errors[j])
                    group_sources.add(sorted_errors[j]['source'])
                    group_indices.add(j)
            else:
                break

        if len(group_sources) >= 2:
            used_indices.update(group_indices)

            time_range = f"{group[0]['timestamp_str']} - {group[-1]['timestamp_str']}"

            correlated_groups.append({
                'time_range': time_range,
                'sources': sorted(list(group_sources)),
                'error_count': len(group),
                'description': f"Errors across {len(group_sources)} services"
            })

    return correlated_groups

def extract_error_patterns(all_errors):
    patterns = []

    for error in all_errors:
        msg = error['message']

        # Identify common patterns
        if 'timeout' in msg.lower():
            if 'connection' in msg.lower():
                patterns.append('Connection timeout')
            elif 'query' in msg.lower():
                patterns.append('Query timeout')
            else:
                patterns.append('Timeout')
        elif 'connection pool' in msg.lower():
            patterns.append('Connection pool exhausted')
        elif 'cache miss' in msg.lower():
            patterns.append('Cache miss')
        elif 'failed to' in msg.lower():
            patterns.append('Operation failed')
        elif 'unavailable' in msg.lower():
            patterns.append('Service unavailable')
        elif 'connection' in msg.lower() and 'lost' in msg.lower():
            patterns.append('Connection lost')
        elif 'memory' in msg.lower():
            patterns.append('Memory issue')
        elif 'disk' in msg.lower():
            patterns.append('Disk issue')
        else:
            patterns.append('Other error')

    pattern_counts = Counter(patterns)
    top_patterns = [
        {'pattern': pattern, 'count': count}
        for pattern, count in pattern_counts.most_common(3)
    ]

    return top_patterns

def generate_timeline(all_errors):
    sorted_errors = sorted(all_errors, key=lambda x: x['timestamp'])

    lines = []
    for error in sorted_errors:
        line = f"{error['timestamp_str']} [{error['source']}] {error['level']} {error['message']}"
        lines.append(line)

    return '\n'.join(lines)

def main():
    log_files = [
        '/app/logs/api.log',
        '/app/logs/database.log',
        '/app/logs/cache.log'
    ]

    all_errors = []
    for log_file in log_files:
        errors = parse_log_file(log_file)
        all_errors.extend(errors)

    total_errors = len(all_errors)
    critical_errors = sum(1 for e in all_errors if e['level'] == 'CRITICAL')
    correlated_groups = find_correlations(all_errors, window_seconds=5)

    top_patterns = extract_error_patterns(all_errors)
    summary = {
        'total_errors': total_errors,
        'critical_errors': critical_errors,
        'correlated_groups': correlated_groups,
        'top_patterns': top_patterns
    }

    with open('/app/error_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    timeline = generate_timeline(all_errors)

    with open('/app/timeline.txt', 'w') as f:
        f.write(timeline)

EOF

python3 /app/analyze_logs.py

if [ ! -f /app/error_summary.json ]; then
    echo "Error: error_summary.json not created"
    exit 1
fi

if [ ! -f /app/timeline.txt ]; then
    echo "Error: timeline.txt not created"
    exit 1
fi

echo "successfully"