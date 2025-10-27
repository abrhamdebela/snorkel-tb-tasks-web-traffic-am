import json
from pathlib import Path
from datetime import datetime


def test_error_summary_exists():
    assert Path("/app/error_summary.json").exists(), "error_summary.json not found"


def test_timeline_exists():
    assert Path("/app/timeline.txt").exists(), "timeline.txt not found"


def test_error_summary_structure():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    required_fields = ["total_errors", "critical_errors", "correlated_groups", "top_patterns"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

def test_error_counts():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    assert data["total_errors"] == 26, f"Expected 26 total errors, got {data['total_errors']}"
    assert data["critical_errors"] == 5, f"Expected 5 critical errors, got {data['critical_errors']}"


def test_correlated_groups():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    assert len(data["correlated_groups"]) >= 3

    for group in data["correlated_groups"]:
        assert "time_range" in group
        assert "sources" in group
        assert len(group["sources"]) >= 2


def test_top_patterns():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    assert len(data["top_patterns"]) == 3, "Should have exactly 3 top patterns"

    for pattern in data["top_patterns"]:
        assert "pattern" in pattern or "type" in pattern
        assert "count" in pattern
        assert isinstance(pattern["count"], int)

    top_pattern = data["top_patterns"][0]
    assert top_pattern["count"] >= 4, "Top pattern should appear at least 4 times"


def test_timeline_format():
    timeline = Path("/app/timeline.txt").read_text()

    lines = timeline.strip().split("\n")
    assert len(lines) >= 26, f"Timeline should have at least 26 lines, got {len(lines)}"

    timestamps = []
    for line in lines:
        if not line.strip():
            continue
        if len(line) >= 19:
            ts_str = line[:19]
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(ts)
            except ValueError:
                pass
    assert timestamps == sorted(timestamps), "Timeline should be in chronological order"


def test_correlation_accuracy():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    found_critical_correlation = False

    for group in data["correlated_groups"]:
        sources = group.get("sources", group.get("logs", []))

        # 3개 이상의 서비스 또는 api+database 조합
        if (len(sources) >= 3) or (set(sources) >= {"api", "database"}):
            found_critical_correlation = True
            break

    assert found_critical_correlation, \
        "Should detect major correlation event around 14:24 or 14:25"


def test_pattern_types():
    with open("/app/error_summary.json") as f:
        data = json.load(f)

    pattern_texts = [
        p.get("pattern", p.get("type", "")).lower()
        for p in data["top_patterns"]
    ]

    common_patterns = ["timeout", "connection", "pool", "cache miss"]

    found = any(
        any(pattern in text for pattern in common_patterns)
        for text in pattern_texts
    )

    assert found, f"Should identify common error patterns like timeout/connection, got: {pattern_texts}"




