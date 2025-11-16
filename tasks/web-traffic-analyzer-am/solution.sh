import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("dataset/access.log")

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3})'
)

TS_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def parse_line(line: str):
    m = LOG_PATTERN.match(line)
    if not m:
        return None
    d = m.groupdict()
    try:
        ts = datetime.strptime(d["ts"], TS_FORMAT)
    except Exception:
        return None

    return {
        "ip": d["ip"],
        "timestamp": ts,
        "method": d["method"],
        "path": d["path"],
        "status": int(d["status"]),
    }


def analyze_log(path: Path):
    ip_counter = Counter()
    url_counter = Counter()
    method_counter = Counter()
    status_cat_counter = Counter()  # 2xx, 3xx, etc.
    per_ip_timestamps = defaultdict(list)
    error_timestamps = []

    with path.open() as f:
        for line in f:
            entry = parse_line(line)
            if not entry:
                continue

            ip = entry["ip"]
            ts = entry["timestamp"]
            method = entry["method"]
            path = entry["path"]
            status = entry["status"]

            ip_counter[ip] += 1
            url_counter[path] += 1
            method_counter[method] += 1
            status_cat_counter[status // 100 * 100] += 1

            per_ip_timestamps[ip].append(ts)
            if 500 <= status < 600:
                error_timestamps.append(ts)

    total_requests = sum(ip_counter.values())
    unique_visitors = len(ip_counter)

    return {
        "total_requests": total_requests,
        "unique_visitors": unique_visitors,
        "top_urls": url_counter.most_common(10),
        "top_ips": ip_counter.most_common(10),
        "method_counts": dict(method_counter),
        "status_categories": dict(status_cat_counter),
        "per_ip_timestamps": per_ip_timestamps,
        "error_timestamps": error_timestamps,
    }


def detect_anomalies(per_ip_timestamps, error_timestamps):
    suspicious_ips = set()
    error_bursts = False

    # very simple O(n^2) sliding window – fine for small datasets
    for ip, ts_list in per_ip_timestamps.items():
        ts_list = sorted(ts_list)
        for i in range(len(ts_list)):
            win_start = ts_list[i]
            count = 1
            for j in range(i + 1, len(ts_list)):
                if (ts_list[j] - win_start).total_seconds() <= 60:
                    count += 1
                else:
                    break
            if count > 100:
                suspicious_ips.add(ip)
                break

    error_timestamps = sorted(error_timestamps)
    for i in range(len(error_timestamps)):
        win_start = error_timestamps[i]
        count = 1
        for j in range(i + 1, len(error_timestamps)):
            if (error_timestamps[j] - win_start).total_seconds() <= 60:
                count += 1
            else:
                break
        if count > 20:
            error_bursts = True
            break

    return suspicious_ips, error_bursts


def main():
    data = analyze_log(LOG_PATH)
    suspicious_ips, error_bursts = detect_anomalies(
        data["per_ip_timestamps"],
        data["error_timestamps"],
    )

    # Human-readable output – tests will just check for key headings
    print("Total requests:", data["total_requests"])
    print("Unique visitors:", data["unique_visitors"])
    print("\nTop URLs:")
    for url, count in data["top_urls"]:
        print(f"  {url}: {count}")

    print("\nTop IPs:")
    for ip, count in data["top_ips"]:
        print(f"  {ip}: {count}")

    print("\nMethod counts:")
    for method, count in data["method_counts"].items():
        print(f"  {method}: {count}")

    print("\nStatus code categories:")
    for cat, count in sorted(data["status_categories"].items()):
        print(f"  {cat}s: {count}")

    print("\nAnomalies:")
    if suspicious_ips:
        print("  High-traffic IPs (>100 req / 60s):", ", ".join(sorted(suspicious_ips)))
    else:
        print("  No high-traffic IP anomalies detected.")

    if error_bursts:
        print("  Detected 5xx error burst ( >20 / 60s ).")
    else:
        print("  No 5xx error bursts detected.")


if __name__ == "__main__":
    main()
