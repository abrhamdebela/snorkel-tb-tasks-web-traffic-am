# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Terminal-Bench (T-Bench) is a benchmark for testing AI agents in real terminal environments. It consists of a dataset of tasks and an execution harness that connects language models to a sandboxed terminal environment.

## Architecture

### Core Component

- **`tasks/`**: Individual task implementations
  - Each task has its own directory with instruction, docker environment, test script, and reference solution
  - Tasks include Python, shell scripts, C, Rust, and other languages

## Common Development Commands

### Running Tasks
```bash
# Run the oracle agent
uv run tb run --task-id "task-name" --agent oracle

# Run specific tasks
uv run tb run --task-id "task-name" --agent terminus --model model-name
```

### Linting and Code Quality
```bash
# Run Ruff linter
uvx ruff check .

# Fix auto-fixable issues
uvx ruff check . --fix
```

### Task Management
```bash
# Create a new task (follow the documentation)
uv run stb tasks create
```

## Development Guidelines

### Python Style
- Python 3.13+ is used
- Use type hints for all functions
- Private methods have `_` prefix
- Use modular design, avoid deep nesting
- Use modern type annotations: `list`, `dict`, `|` instead of `List`, `Dict`, `Union`

### File Structure
- Tasks are in `tasks/` directory
- Each task must have:
  - An instruction in English
  - A test script to verify completion
  - A reference solution

### Dependencies
- Project uses `uv` for dependency management
- Dependencies are specified in `pyproject.toml`
- Use `uv sync` to install dependencies

## Git Workflow

- Main branch: `main`
- Pull requests are required for changes
- GitHub Actions run tests and linting on PRs

## Notes

- Docker is required for running the terminal sandbox