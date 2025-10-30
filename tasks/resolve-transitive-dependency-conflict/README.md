# Resolve Transitive Dependency Conflict

## Task Overview

This task challenges an AI agent to diagnose and resolve a Python dependency conflict caused by incompatible transitive dependencies.

**The Problem:** Your application requires both PackageA v2.0 and PackageB v1.0. However, PackageA v2.0 depends on PackageC v2.0, while PackageB v1.0 depends on PackageC v1.0. Since Python cannot install two versions of the same package simultaneously, `pip install` fails with a dependency conflict error. The agent must identify this conflict and determine that downgrading PackageA to v1.0 (which is compatible with PackageC v1.0) resolves the issue.

## Environment Setup

The task environment contains:
- A `requirements.txt` file specifying: `PackageA==2.0` and `PackageB==1.0`
- A local package repository at `/packages` with all available versions

**Dependency Chain:**
- `PackageA==2.0` → requires `PackageC>=2.0`
- `PackageA==1.0` → requires `PackageC==1.0`
- `PackageB==1.0` → requires `PackageC==1.0`
- `PackageC` has no dependencies

**The Conflict:** PackageA v2.0 and PackageB v1.0 cannot coexist because they require incompatible versions of PackageC.

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
- `PackageA-1.0.tar.gz` (depends on `PackageC==1.0`)
- `PackageA-2.0.tar.gz` (depends on `PackageC>=2.0`)
- `PackageB-1.0.tar.gz` (depends on `PackageC==1.0`)
- `PackageC-1.0.tar.gz` (no dependencies)
- `PackageC-2.0.tar.gz` (no dependencies)

## Testing

The test suite validates:
1. The `requirements.txt` file was modified to use `PackageA==1.0`
2. The file still contains exactly 2 packages (no additions or deletions)
3. All packages are successfully installed in the environment
4. The final environment has the correct compatible versions (A=1.0, B=1.0, C=1.0)
5. The conflicting `PackageC==2.0` is not installed

## Technical Notes

- All packages are served from a local directory (`/packages`) to ensure reproducibility and prevent external network access
- Install packages using: `pip install -r requirements.txt --find-links /packages`
- The `pipdeptree` tool is pre-installed for dependency tree visualization
- This task tests practical knowledge of Python's pip dependency resolver and constraint satisfaction
