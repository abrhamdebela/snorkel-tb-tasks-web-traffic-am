# Resolve Transitive Dependency Conflict

## Task Overview

This task challenges an AI agent to diagnose and resolve a **diamond dependency conflict** in Python - a more complex scenario than a simple version conflict.

**The Problem:** Your application requires both PackageA v2.0 and PackageB v1.0. This creates a diamond dependency problem:
- PackageA v2.0 requires PackageC v2.0 and PackageD v1.0+
- PackageB v1.0 requires PackageC v1.0 and PackageD v1.0+
- PackageD v2.0 requires PackageC v2.0
- PackageD v1.0 requires PackageC v1.0

When pip tries to resolve dependencies, it attempts to use PackageD v2.0 (the latest matching v1.0+), but this conflicts with PackageB's requirement for PackageC v1.0. The agent must trace through this dependency chain and determine that downgrading PackageA to v1.0 resolves all conflicts.

## Environment Setup

The task environment contains:
- A `requirements.txt` file specifying: `PackageA==2.0` and `PackageB==1.0`
- A local package repository at `/packages` with all available versions

**Dependency Chain (Diamond Problem):**
```
         PackageA v2.0          PackageB v1.0
              |                       |
              v                       v
       PackageC>=2.0            PackageC==1.0
       PackageD>=1.0            PackageD>=1.0
              |                       |
              v                       v
         PackageD v2.0  -----> PackageC>=2.0
```

**Available Versions:**
- `PackageA`: v1.0 (requires PackageC==1.0, PackageD>=1.0) | v2.0 (requires PackageC>=2.0, PackageD>=1.0)
- `PackageB`: v1.0 only (requires PackageC==1.0, PackageD>=1.0)
- `PackageC`: v1.0 | v2.0 (no dependencies)
- `PackageD`: v1.0 (requires PackageC==1.0) | v2.0 (requires PackageC>=2.0)

**The Conflict:** This is a diamond dependency where multiple paths lead to PackageC. Pip will try to use PackageD v2.0 (latest), which forces PackageC v2.0, but PackageB explicitly requires PackageC v1.0.

## Success Criteria

The agent must:
1. Identify the dependency conflict by attempting to install the requirements
2. Diagnose the root cause (incompatible transitive dependencies on PackageC)
3. Investigate available package versions in `/packages`
4. Modify `requirements.txt` to use `PackageA==1.0` (which is compatible with `PackageB==1.0`)
5. Successfully install all dependencies without conflicts

## Skills Tested

This task evaluates the agent's ability to:
1. **Debug** - Read and interpret pip error messages showing dependency conflicts
2. **Investigate** - List and examine available package versions in the repository
3. **Reason** - Trace transitive dependencies to identify the root cause
4. **Resolve** - Select compatible package versions that satisfy all constraints

## Package Structure

The local repository `/packages` contains:
- `PackageA-1.0.tar.gz` (depends on `PackageC==1.0`, `PackageD>=1.0`)
- `PackageA-2.0.tar.gz` (depends on `PackageC>=2.0`, `PackageD>=1.0`)
- `PackageB-1.0.tar.gz` (depends on `PackageC==1.0`, `PackageD>=1.0`)
- `PackageC-1.0.tar.gz` (no dependencies)
- `PackageC-2.0.tar.gz` (no dependencies)
- `PackageD-1.0.tar.gz` (depends on `PackageC==1.0`)
- `PackageD-2.0.tar.gz` (depends on `PackageC>=2.0`)

## Testing

The test suite validates:
1. The `requirements.txt` file was modified to use `PackageA==1.0`
2. The file still contains exactly 2 packages (no additions or deletions)
3. All packages are successfully installed in the environment
4. The final environment has the correct compatible versions (A=1.0, B=1.0, C=1.0, D=1.0)
5. The conflicting versions (`PackageC==2.0` and `PackageD==2.0`) are not installed

## Technical Notes

- All packages are served from a local directory (`/packages`) to ensure reproducibility and prevent external network access
- Install packages using: `pip install -r requirements.txt --find-links /packages`
- The `pipdeptree` tool is pre-installed for dependency tree visualization
- This task tests understanding of diamond dependencies, transitive dependency resolution, and constraint satisfaction
- **Difficulty: Hard** - Requires tracing multiple dependency paths and understanding how pip's resolver chooses versions
