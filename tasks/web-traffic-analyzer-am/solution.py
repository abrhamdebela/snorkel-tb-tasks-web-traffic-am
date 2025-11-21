import re
import sys
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path

# Default input log path used by the harness
LOG_PATH = Path("/workspace/dataset/access.log")


# Output file the tests expect
OUTPUT_PATH = Path("/tmp/web_traffic_report.txt")

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3})'
)

TS_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def parse_line(line: str):
    """Parse a single Apache-style access log line."""
    m = LOG_PATTERN.match(line)
    if not m:
        return None

    d = m.groupdict()
    try:
        ts = datetime.strptime(d["ts"], TS_FORMAT)
    except Exception:
        # Skip lines with bad timestamps
        return None

    return {
        "ip": d["ip"],
        "timestamp": ts,
        "method": d["method"],
        "path": d["path"],
        "status": int(d["status"]),
    }


def analyze_log(path: Path):
    """Compute basic traffic stats and simple anomalies from a log file."""
    total_requests = 0
    unique_ips = set()
    url_counter = Counter()
    ip_counter = Counter()
    method_counter = Counter()
    status_category_counter = Counter()  # "2xx", "3xx", etc.

    # Anomaly detection state
    ip_windows = defaultdict(deque)  # ip -> deque[timestamps]
    error_window = deque()           # deque[timestamps of 5xx]
    anomalies = {
        "high_traffic_ips": [],      # (ip, start, end, count)
        "error_bursts": []           # (start, end, count)
    }

    window_size = timedelta(seconds=60)

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            entry = parse_line(line)
            if not entry:
                continue

            ip = entry["ip"]
            ts = entry["timestamp"]
            method = entry["method"]
            url_path = entry["path"]
            status = entry["status"]

            total_requests += 1
            unique_ips.add(ip)
            url_counter[url_path] += 1
            ip_counter[ip] += 1
            method_counter[method] += 1

            status_category = f"{status // 100}xx"
            status_category_counter[status_category] += 1

            # --- Anomaly: per-IP > 100 requests in 60 seconds ---
            dq = ip_windows[ip]
            dq.append(ts)
            while dq and ts - dq[0] > window_size:
                dq.popleft()
            if len(dq) > 100:
                anomalies["high_traffic_ips"].append(
                    (ip, dq[0], dq[-1], len(dq))
                )

            # --- Anomaly: >20 5xx errors in 60 seconds ---
            if 500 <= status < 600:
                error_window.append(ts)
                while error_window and ts - error_window[0] > window_size:
                    error_window.popleft()
                if len(error_window) > 20:
                    anomalies["error_bursts"].append(
                        (error_window[0], error_window[-1], len(error_window))
                    )

    return {
        "total_requests": total_requests,
        "unique_visitors": len(unique_ips),
        "top_urls": url_counter.most_common(10),
        "top_ips": ip_counter.most_common(10),
        "method_counts": method_counter,
        "status_categories": status_category_counter,
        "anomalies": anomalies,
    }


def format_report(metrics):
    """Turn metrics into the human-readable report the tests assert on."""
    lines = []

    lines.append(f"Total requests: {metrics['total_requests']}")
    lines.append(f"Unique visitors: {metrics['unique_visitors']}")
    lines.append("")

    lines.append("Top URLs:")
    for url, count in metrics["top_urls"]:
        lines.append(f"  {url} - {count}")
    if not metrics["top_urls"]:
        lines.append("  (none)")
    lines.append("")

    lines.append("Top IPs:")
    for ip, count in metrics["top_ips"]:
        lines.append(f"  {ip} - {count}")
    if not metrics["top_ips"]:
        lines.append("  (none)")
    lines.append("")

    lines.append("Method counts:")
    for method, count in sorted(metrics["method_counts"].items()):
        lines.append(f"  {method}: {count}")
    if not metrics["method_counts"]:
        lines.append("  (none)")
    lines.append("")

    lines.append("Status code categories:")
    for cat, count in sorted(metrics["status_categories"].items()):
        lines.append(f"  {cat}: {count}")
    if not metrics["status_categories"]:
        lines.append("  (none)")
    lines.append("")

    lines.append("Anomalies:")
    any_anom = False

    if metrics["anomalies"]["high_traffic_ips"]:
        any_anom = True
        lines.append("  High traffic IPs (>100 req in 60s):")
        for ip, start, end, count in metrics["anomalies"]["high_traffic_ips"]:
            lines.append(
                f"    {ip} - {count} requests between "
                f"{start.isoformat()} and {end.isoformat()}"
            )

    if metrics["anomalies"]["error_bursts"]:
        any_anom = True
        lines.append("  5xx error bursts (>20 errors in 60s):")
        for start, end, count in metrics["anomalies"]["error_bursts"]:
            lines.append(
                f"    {count} errors between "
                f"{start.isoformat()} and {end.isoformat()}"
            )

    if not any_anom:
        lines.append("  None detected.")

    return "\n".join(lines)


def main():
    # Optional CLI arg to override log path
    if len(sys.argv) > 1:
        log_path = Path(sys.argv[1])
    else:
        log_path = LOG_PATH

    metrics = analyze_log(log_path)
    report = format_report(metrics)

    # Write report where tests expect it
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report + "\n", encoding="utf-8")

    # Also print to stdout (useful when you run manually)
    print(report)


if __name__ == "__main__":
    main()
