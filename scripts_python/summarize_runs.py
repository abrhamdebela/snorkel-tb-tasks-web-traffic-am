#!/usr/bin/env python3
from collections import defaultdict
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import os

RUNS_ROOT = Path("/tmp/results").resolve()

TIMEOUT_KEYS = {
    "timeout",
    "agent_timeout",
    "test_timeout",
    "timed_out",
    "deadline_exceeded",
}


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


def get_difficulty(agents_summary: Dict[str, Dict[str, Any]]) -> str:
    # Ignore NOP and Oracle for difficulty calculation
    accuracies = [
        agent_summary["accuracy"]
        for agent, agent_summary in agents_summary.items()
        if agent not in ["nop", "oracle"]
    ]
    if any(accuracy < 0.4 for accuracy in accuracies):
        return "hard"
    elif any(accuracy < 0.6 for accuracy in accuracies):
        return "medium"
    elif any(accuracy < 0.8 for accuracy in accuracies):
        return "easy"
    else:
        return "trivial"


def main():
    if not RUNS_ROOT.exists():
        print(f"No runs directory found at {RUNS_ROOT}")
        return

    batch_dirs = [
        d
        for d in RUNS_ROOT.iterdir()
        if d.is_dir() and d.name.startswith("test-result-")
    ]
    print(batch_dirs)
    batch_dirs.sort()

    all_results: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for bd in batch_dirs:
        agent, task, run = parse_batch_name(bd)
        results_json = safe_read_json(bd / "results.json")
        all_results[task][agent].extend(results_json.get("results", []))

    summary: Dict[str, Dict[str, Any]] = defaultdict(dict)
    for task, results_by_agent in all_results.items():
        agents_summary: Dict[str, Dict[str, Any]] = defaultdict(dict)
        for agent, task_results in results_by_agent.items():
            is_resolveds = []
            for result in task_results:
                # Treat None as False (unresolved)
                is_resolved = result["is_resolved"]
                is_resolveds.append(is_resolved if is_resolved is not None else False)
            agents_summary[agent]["accuracy"] = sum(is_resolveds) / len(is_resolveds)
            if len(is_resolveds) >= 5:
                agents_summary[agent]["pass_at_5"] = pass_at_k_estimator(
                    len(is_resolveds), sum(is_resolveds), 5
                )
            else:
                agents_summary[agent]["pass_at_5"] = "N/A"
            agents_summary[agent]["n_runs"] = len(task_results)
        summary[task]["agents"] = agents_summary
        summary[task]["difficulty"] = get_difficulty(agents_summary)
    with open("summary-of-runs-comment.md", "w") as f:
        for task, task_summary in summary.items():
            f.write(f'## Summary of Runs for "{task}":\n')
            f.write(f"Difficulty: {task_summary['difficulty']}\n")
            f.write("| Agent/Model | # of runs | Accuracy | Pass@5 |\n")
            f.write("|-------------|------------|----------|--------|\n")
            for agent, data in task_summary["agents"].items():
                f.write(
                    f"| {agent} | {data['n_runs']} | {data['accuracy']} | {data['pass_at_5']} |\n"
                )
    # Send the difficulty of the last task to $GITHUB_OUTPUT
    # Note: last task but it should be fine as a PR should only contain one task
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"difficulty=difficulty:{summary[task]['difficulty']}\n")


if __name__ == "__main__":
    main()
