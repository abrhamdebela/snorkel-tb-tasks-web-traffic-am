# Resolve Multi-Layered, Obfuscated dependency conflict

## Task Overview

This task challenges an AI agent to diagnose and resolve a **multi-layered, obfuscated dependency conflict** scenario - an expert-level challenge that combines three interlocking layers of complexity designed to mislead and confuse. This represents a realistic "nightmare scenario" created by a chaotic development team.

**The Nightmare:** Your application has 4 packages in `requirements.txt`, but `pip install` is failing with cryptic error messages pointing to multiple packages. The errors are confusing, misleading, and don't reveal the true nature of the problem.

## The Three Layers of Complexity

### Layer 1: The Red Herring (Obvious Shallow Conflict)

The agent will immediately see this conflict:
- **PackageA v2.0** requires **PackageB>=2.0**
- **PackageH v1.0** requires **PackageB==1.0**
- **CONFLICT:** Incompatible PackageB versions

This is the **obvious** conflict that will draw the agent's attention first. The natural solution appears to be downgrading PackageA to v1.0.

**But wait...** PackageA v1.0 has a **critical security vulnerability (CVE-2024-XXXXX)**! The task instructions explicitly warn against downgrading. This creates a moral dilemma and makes the agent reluctant to try the obvious solution.

### Layer 2: The Deep Conflict (3-Level Dependency Chain)

Hidden beneath the red herring is a **3-level deep transitive dependency conflict**:

**When PackageA==2.0 is selected:**
```
PackageA v2.0 ──→ PackageB>=2.0 ──→ PackageD>=2.0
                                      │
                                      ↓
                                 PackageD v2.0 ──→ PackageE>=2.0
                                                        │
                                                        ↓
                                                   PackageE v2.0 ──→ PackageC>=2.0
```

**But:**
- **PackageF v1.0** requires **PackageC==1.0**
- **CONFLICT:** PackageC needs >=2.0 from the chain but ==1.0 from PackageF

This conflict is **invisible** until the agent resolves the red herring. Only after downgrading PackageA to v1.0 does this deep conflict become apparent.

### Layer 3: The Environmental Trap (Obfuscated Booby Trap)

The most evil layer is **PackageG**, which has a **conditional dependency** based on an environment variable:

**PackageG's setup.py:**
```python
import os
solve_conflict = os.environ.get("SOLVE_G_CONFLICT", "").strip()
if solve_conflict == "true":
    deps = []  # No conflict if properly set
else:
    deps = ["PackageC==1.0"]  # Creates conflict with A v2.0 path
```

The **trap:** The Dockerfile sets `ENV SOLVE_G_CONFLICT="true​"` with a **ZERO-WIDTH SPACE character (U+200B)** after "true". This invisible character makes the string comparison fail, so PackageG **always** requires PackageC==1.0, creating additional confusion.

The agent must use **forensic tools** like `env | od -c` or `env | cat -A` to discover this invisible character.

## The Investigation Journey

A successful agent must navigate this maze in a specific order:

1. **Initial Failure:** See the red herring conflict (A v2.0 vs H v1.0 over B)
2. **Reluctant Downgrade:** Overcome the security warning and try downgrading A to v1.0
3. **Second Failure:** Discover the deeper conflicts involving PackageC
4. **Forensic Investigation:** Extract and examine PackageG's setup.py to understand its conditional behavior
5. **Environmental Discovery:** Use forensic tools to discover the zero-width space in SOLVE_G_CONFLICT
6. **Deep Dependency Tracing:** Trace the full A→B→D→E→C dependency chain
7. **Final Realization:** Understand that all conflicts converge on PackageC==1.0 when A==1.0
8. **Accept the Trade-off:** Conclude that PackageA==1.0 is the only solution despite the security risk

## Environment Setup

The task environment contains:
- A `requirements.txt` file with: `PackageA==2.0`, `PackageF==1.0`, `PackageG==1.0`, `PackageH==1.0`
- A local package repository at `/packages` with all package versions
- An environment variable `SOLVE_G_CONFLICT="true​"` (with hidden zero-width space)
- A business-critical script `/app/run_analysis.py` that imports both PackageA and PackageF

## Complete Dependency Architecture

**Available Packages:**
- **PackageA:** v1.0 (requires B>=1.0, **HAS SECURITY VULNERABILITY**) | v2.0 (requires B>=2.0, **SECURE**)
- **PackageB:** v1.0 (requires C==1.0, D>=1.0) | v2.0 (requires C>=2.0, D>=2.0)
- **PackageC:** v1.0 | v2.0 (leaf package, no dependencies)
- **PackageD:** v1.0 (requires E==1.0) | v2.0 (requires E>=2.0)
- **PackageE:** v1.0 (requires C==1.0) | v2.0 (requires C>=2.0)
- **PackageF:** v1.0 (requires C==1.0)
- **PackageG:** v1.0 (conditionally requires C==1.0 if SOLVE_G_CONFLICT != "true")
- **PackageH:** v1.0 (requires B==1.0)

**The Final Solution:**
```
PackageA==1.0  # Downgraded to resolve red herring (security trade-off)
PackageF==1.0  # Unchanged
PackageG==1.0  # Unchanged
PackageH==1.0  # Unchanged
```

**Why this works:**
```
PackageA v1.0 → PackageB>=1.0 (pip selects v1.0 for compatibility)
PackageB v1.0 → PackageC==1.0, PackageD>=1.0 (pip selects v1.0)
PackageD v1.0 → PackageE==1.0
PackageE v1.0 → PackageC==1.0
PackageF v1.0 → PackageC==1.0
PackageG v1.0 → PackageC==1.0 (due to broken env var)
PackageH v1.0 → PackageB==1.0

ALL PATHS CONVERGE ON: PackageB v1.0, PackageC v1.0 → COMPATIBLE!
```

## Success Criteria

The agent must:
1. Identify the red herring conflict (A vs H over B)
2. Investigate the deep conflict (A→B→D→E→C vs F→C)
3. Discover PackageG's conditional dependency mechanism
4. Use forensic tools to identify the zero-width space in SOLVE_G_CONFLICT
5. Trace the complete dependency tree across all 8 packages
6. Recognize that PackageA==1.0 is the only solution despite security concerns
7. Successfully install all 8 packages (A, B, C, D, E, F, G, H) with compatible versions

## Testing

The test suite validates:
1. The `requirements.txt` file was modified (PackageA changed from 2.0 to 1.0)
2. The file still contains exactly 4 packages (no additions or deletions)
3. All 8 packages are successfully installed (4 direct + 4 transitive dependencies)
4. All packages exist in site-packages (prevents faking pip output)
5. No dependency conflicts remain (pip can resolve dependencies successfully)

## Skills Tested

This task evaluates the agent's ability to:
1. **Diagnose** - Identify multiple interlocking dependency conflicts from cryptic error messages
2. **Investigate** - Extract and examine package source code (setup.py) to understand behavior
3. **Forensic Analysis** - Use low-level tools (od, cat -A) to discover hidden environmental issues
4. **Trace** - Follow multi-level transitive dependency chains (3 levels deep)
5. **Reason** - Understand that "obvious" conflicts may be red herrings masking deeper problems
6. **Prioritize** - Make difficult trade-offs between security and functionality constraints
7. **Persist** - Continue investigating after initial solutions fail

## Technical Notes

- All packages are served from a local directory (`/packages`) to ensure reproducibility
- Install packages using: `pip install -r requirements.txt --find-links /packages`
- The `pipdeptree` tool is pre-installed for dependency tree visualization
- PackageG's conditional dependency is evaluated **during package installation**, not runtime
- The zero-width space character (U+200B) is invisible in most text editors
- **Difficulty: Expert** - This task requires forensic investigation skills beyond normal dependency resolution
- **Expected Time:** 15-30 minutes for an experienced developer who recognizes the patterns

## Why This is "Over the Top"

This task is intentionally designed to be **misleadingly complex**:

1. **Red Herring:** The obvious conflict is NOT the real problem
2. **Security FUD:** The security warning creates hesitation to try the correct solution
3. **Hidden Layers:** Each "solution" reveals a new problem
4. **Environmental Sabotage:** The broken environment variable is forensically hidden
5. **Cascading Failures:** Error messages point to multiple packages, obscuring the root cause
6. **Business Constraints:** The critical script creates pressure to keep specific versions
7. **Mental Exhaustion:** Designed to send agents down multiple dead ends before finding the truth

This simulates a real-world "dependency conflict" scenario created by a tired, overworked team making incremental changes without understanding the full dependency graph.
