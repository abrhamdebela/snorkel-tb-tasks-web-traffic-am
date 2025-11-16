from pathlib import Path
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
import sys
import re

# Default path used by the harness
LOG_PATH = Path("dataset/access.log")

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)[^"]*"\s+'
    r'(?P<status>\d{3})\s+\S+'
)

TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def parse_line(line: str):
    m = LOG_PATTERN.match(line)
    if not m:
        return None

    try:
        ip = m.group("ip")
        ts = datetime.strptime(m.group("time"), TIME_FORMAT)
        method = m.group("method")
        path = m.group("path")
        status = int(m.group("status"))
    except Exception:
        return None

    return ip, ts, method, path, status


def analyze_log(path: Path):
    total_requests = 0
    unique_ips = set()
    url_counter = Counter()
    ip_counter = Counter()
    method_counter = Counter()
    status_category_counter = Counter()

    # Anomaly detection data structures
    ip_windows = defaultdict(deque)         # ip -> timestamps
    error_window = deque()                  # timestamps of 5xx
    anomalies = {
        "high_traffic_ips": [],             # (ip, start, end, count)
        "error_bursts": []                  # (start, end, count)
    }

    window_size = timedelta(seconds=60)

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                # Skip malformed line
                continue

            ip, ts, method, url_path, status = parsed

            total_requests += 1
            unique_ips.add(ip)
            url_counter[url_path] += 1
            ip_counter[ip] += 1
            method_counter[method] += 1

            status_category = f"{status // 100}xx"
            status_category_counter[status_category] += 1

            # --- Anomaly: per-IP > 100 req in 60s ---
            dq = ip_windows[ip]
            dq.append(ts)
            # Drop timestamps older than 60s from current
            while dq and ts - dq[0] > window_size:
                dq.popleft()
            if len(dq) > 100:
                anomalies["high_traffic_ips"].append(
                    (ip, dq[0], dq[-1], len(dq))
                )

            # --- Anomaly: 5xx burst > 20 in 60s ---
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
                f"    {ip} - {count} requests between {start.isoformat()} and {end.isoformat()}"
            )

    if metrics["anomalies"]["error_bursts"]:
        any_anom = True
        lines.append("  5xx error bursts (>20 errors in 60s):")
        for start, end, count in metrics["anomalies"]["error_bursts"]:
            lines.append(
                f"    {count} errors between {start.isoformat()} and {end.isoformat()}"
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
    print(report)


if __name__ == "__main__":
    main()
