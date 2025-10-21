#!/usr/bin/env python3
from collections import defaultdict
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

RUNS_ROOT = Path("/tmp/results").resolve()

TIMEOUT_KEYS = {"timeout", "agent_timeout", "test_timeout", "timed_out", "deadline_exceeded"}

def parse_batch_name(batch_dir: Path):
    """Example: test-result-claude-code-4-5-sonnet-2"""
    agent_run = batch_dir.name.replace("test-result-", "")
    agent, task, run = agent_run.split("_")
    return agent, task, run

def safe_read_json(p: Path) -> Optional[Dict[str, Any]]:
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def pass_at_k_estimator(n: int, c: int, k: int) -> float:
    """Calculates 1 - comb(n - c, k) / comb(n, k)."""
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))
    

def main():
    if not RUNS_ROOT.exists():
        print(f"No runs directory found at {RUNS_ROOT}")
        return

    batch_dirs = [d for d in RUNS_ROOT.iterdir() if d.is_dir() and d.name.startswith("test-result-")]
    print(batch_dirs)
    batch_dirs.sort()

    all_results: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for bd in batch_dirs:
        agent, task, run = parse_batch_name(bd)
        results_json = safe_read_json(bd / "results.json")
        all_results[task][agent].extend(results_json.get("results", []))
    
    summary: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: defaultdict(dict))
    for task, results_by_agent in all_results.items():
        for agent, task_results in results_by_agent.items():
            is_resolveds = []
            for result in task_results:
                is_resolveds.append(result["is_resolved"])
            summary[task][agent]["accuracy"] = sum(is_resolveds) / len(is_resolveds)
            if len(is_resolveds) >= 5:
                summary[task][agent]["pass_at_5"] = pass_at_k_estimator(len(is_resolveds), sum(is_resolveds), 5)
            else:
                summary[task][agent]["pass_at_5"] = "N/A"
            summary[task][agent]["n_runs"] = len(task_results)
    with open("summary-of-runs-comment.md", "w") as f:
        for task, results_by_agent in summary.items():
            f.write(f"## Summary of Runs for \"{task}\":\n")
            f.write("| Agent/Model | # of runs | Accuracy | Pass@5 |\n")
            f.write("|-------------|------------|----------|--------|\n")
            for agent, data in results_by_agent.items():
                f.write(f"| {agent} | {data['n_runs']} | {data['accuracy']} | {data['pass_at_5']} |\n")

if __name__ == "__main__":
    main()