# Resolve Multi-Layered, Obfuscated dependency conflict

## Task Overview

This task challenges an AI agent to diagnose and resolve a **multi-layered, obfuscated dependency conflict** scenario - a NIGHTMARE-level challenge that combines six interlocking layers of complexity designed to mislead and confuse. This represents a realistic "dependency hell" created by a chaotic enterprise environment with conflicting business requirements.

**The Nightmare:** Your application has 9 packages in `requirements.txt`, but `pip install` is failing with cryptic error messages pointing to multiple packages. The errors are confusing, misleading, and don't reveal the true nature of the problem. Multiple business constraints create impossible trade-offs.

## The Six Layers of Complexity

### Layer 1: The Red Herring (Obvious Shallow Conflict)

The agent will immediately see this conflict:
- **PackageA v7.0.3** requires **PackageB>=6.0.0**
- **PackageH v4.2.6** requires **PackageB==0.9.4**
- **CONFLICT:** Incompatible PackageB versions

This is the **obvious** conflict that will draw the agent's attention first. The natural solution appears to be downgrading PackageA to v1.4.7.

**But wait...** PackageA v1.4.7 has a **critical security vulnerability (CVE-2024-XXXXX)**! The task instructions explicitly warn against downgrading. This creates a moral dilemma and makes the agent reluctant to try the obvious solution.

### Layer 2: The Deep Conflict (5-Level Dependency Chain)

Hidden beneath the red herring is a **5-level deep transitive dependency conflict**:

**When PackageA==7.0.3 is selected:**
```
PackageA v7.0.3 ──→ PackageB>=6.0.0 ──→ PackageD>=5.0.0
                                        │
                                        ↓
                                   PackageD v5.2.0 ──→ PackageE>=4.0.0
                                                     │
                                                     ↓
                                                PackageE v4.0.1 ──→ PackageC>=3.1.0
```

**But:**
- **PackageF v2.8.9** requires **PackageC==0.7.3**
- **CONFLICT:** PackageC needs >=3.1.0 from the chain but ==0.7.3 from PackageF

This conflict is **invisible** until the agent resolves the red herring. Only after downgrading PackageA to v1.4.7 does this deep conflict become apparent.

### Layer 3: The Environmental Traps (Multiple Types of Sabotage)

The most evil layer involves **four packages** with **conditional dependencies** based on environment variables with **different types of traps**:

**PackageG's setup.py:**
```python
import os
solve_conflict = os.environ.get("SOLVE_G_CONFLICT", "").strip()
if solve_conflict == "true":
    deps = []  # No conflict if properly set
else:
    deps = ["PackageC==0.7.3"]  # Creates conflict with A v7.0.3 path
```

**PackageI's setup.py:**
```python
import os
enable_opt = os.environ.get("ENABLE_I_OPTIMIZATION", "").strip()
if enable_opt == "true":
    deps = ["PackageD>=4.0.0"]  # Optimized path
else:
    deps = ["PackageD>=1.0.0"]  # Creates conflict with older PackageD versions
```

**PackageK's setup.py:**
```python
import os
license_key = os.environ.get("LICENSE_KEY", "").strip()
if license_key == "VALID_LICENSE_2025":
    deps = ["PackageF>=2.8.0"]  # Licensed features
else:
    deps = ["PackageF>=2.0.0"]  # Fallback to free features
```

**PackageL's setup.py:**
```python
import os
platform_target = os.environ.get("PLATFORM_TARGET", "").strip()
if platform_target == "windows":
    deps = ["PackageG>=3.5.0"]  # Windows-specific features
else:
    deps = ["PackageG>=3.0.0"]  # Cross-platform fallback
```

The **traps:** The Dockerfile sets these with **multiple types of sabotage**:
- `SOLVE_G_CONFLICT="true​"` (zero-width space)
- `ENABLE_I_OPTIMIZATION="true​"` (zero-width space)
- `LICENSE_KEY="VALID_LІCENSE_2025"` (unicode homoglyph: CYRILLIC 'І' instead of LATIN 'I')
- `PLATFORM_TARGET="linux​"` (zero-width space)

The agent must use **forensic tools** like `env | od -c` or `env | cat -A` to discover these different types of hidden characters.

### Layer 4: The Configuration File Trap

**PackageM v3.0.0** reads `/app/package_config.json` during installation:

```python
import json
import os
config_deps = []
config_file = "/app/package_config.json"
if os.path.exists(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
        if config.get("enable_experimental", False):
            config_deps = ["PackageH>=4.0.0"]
```

The config file exists and looks normal, but the agent must examine it forensically to understand its impact on PackageM's dependencies.

### Layer 5: The Compliance and Maintenance Constraints

**PackageJ v2.0.0** has **regulatory compliance requirements** and cannot be changed. It requires:
- PackageE>=1.0.0
- PackageC>=0.5.0

**PackageM v3.0.0** has **extensive custom patches** and cannot be changed. It requires:
- PackageI>=1.0.0
- Conditionally PackageH>=4.0.0 (from config file)

These force the entire ecosystem to use older versions, conflicting with optimization paths.

### Layer 6: The Cost and Platform Constraints

**PackageK v1.0.0** has a **$50,000 annual licensing fee**. The agent should prefer v0.9.8 (free).

**PackageL v2.1.0** is **Windows-only**. For Linux production deployment, the agent should prefer v1.8.5 (cross-platform).

These create additional trade-off decisions that conflict with other constraints.

## The Investigation Journey

A successful agent must navigate this nightmare in a specific order:

1. **Initial Failure:** See the red herring conflict (A v7.0.3 vs H v4.2.6 over B)
2. **Reluctant Downgrade:** Overcome the security warning and try downgrading A to v1.4.7
3. **Second Failure:** Discover the deeper conflicts involving PackageC
4. **Forensic Investigation:** Extract and examine PackageG, I, K, L's setup.py to understand their conditional behavior
5. **Environmental Discovery:** Use forensic tools to discover zero-width spaces in SOLVE_G_CONFLICT and ENABLE_I_OPTIMIZATION
6. **Advanced Environmental Discovery:** Discover unicode homoglyph in LICENSE_KEY and control character in PLATFORM_TARGET
7. **Configuration Investigation:** Examine package_config.json to understand PackageM's conditional dependencies
8. **Compliance Recognition:** Understand PackageJ v2.0.0 and PackageM v3.0.0 cannot be changed
9. **Cost and Platform Analysis:** Evaluate PackageK licensing costs and PackageL platform compatibility
10. **Deep Dependency Tracing:** Trace the full A→B→D→E→C dependency chain and understand all conflicts
11. **Comprehensive Trade-offs:** Accept that PackageA, I, K, L must all be downgraded despite security, performance, cost, and platform concerns
12. **Final Realization:** Understand that all conflicts converge on compatible older versions when all constraints are accepted

## Environment Setup

The task environment contains:
- A `requirements.txt` file with: `PackageA>=7.0.0,<8.0.0`, `PackageF==2.8.9`, `PackageG>=3.5.0,<4.0.0`, `PackageH>=4.2.0,<5.0.0`, `PackageI>=3.1.0,<4.0.0`, `PackageJ>=2.0.0,<3.0.0`, `PackageK>=1.0.0,<2.0.0`, `PackageL>=2.1.0,<3.0.0`, `PackageM>=3.0.0,<4.0.0`
- A local package repository at `/packages` with all package versions
- Environment variables with multiple types of traps: `SOLVE_G_CONFLICT="true​"` (zero-width space), `ENABLE_I_OPTIMIZATION="true​"` (zero-width space), `LICENSE_KEY="VALID_LІCENSE_2025"` (unicode homoglyph), `PLATFORM_TARGET="linux​"` (zero-width space)
- A configuration file `/app/package_config.json` that affects PackageM's dependencies
- A business-critical script `/app/run_analysis.py` that imports PackageA, PackageF, PackageI, and PackageJ

## Complete Dependency Architecture

**Available Packages:**
- **PackageA:** v1.4.7 (requires B>=0.9.0,<4.0, **HAS SECURITY VULNERABILITY**) | v2.9.1 | v4.3.2 | v5.8.6 | v7.0.3 (requires B>=6.0.0, **SECURE**)
- **PackageB:** v0.9.4 (requires C==0.7.3, D>=2.0) | v1.8.3 | v2.7.5 | v3.5.1 | v4.2.8 | v5.6.7 | v6.1.2 (requires C>=3.1.0, D>=5.0.0)
- **PackageC:** v0.5.2 | v0.7.3 | v1.1.9 | v2.4.1 | v3.1.4 | v4.0.8 (leaf packages, no dependencies)
- **PackageD:** v1.9.2 (requires E==0.8.1) | v2.3.1 (requires E==1.2.8) | v3.7.4 | v4.1.6 (requires E>=2.5.0) | v5.2.0 | v6.0.9 (require E>=4.0.0)
- **PackageE:** v0.8.1 (requires C==0.5.2) | v1.2.8 (requires C==0.7.3) | v2.5.3 | v3.3.7 | v4.0.1 (requires C>=3.1.0)
- **PackageF:** v2.8.9 (requires C==0.7.3)
- **PackageG:** v3.5.2 (conditionally requires C==0.7.3 if SOLVE_G_CONFLICT != "true")
- **PackageH:** v4.2.6 (requires B>=0.9.0,<1.0)
- **PackageI:** v1.2.3 (requires D>=1.0.0, **HAS PERFORMANCE ISSUES**) | v2.7.4 | v3.1.4 (conditionally requires D>=4.0.0 if ENABLE_I_OPTIMIZATION == "true", else D>=1.0.0)
- **PackageJ:** v2.0.0 (requires E>=1.0.0, C>=0.5.0, **COMPLIANCE REQUIRED - CANNOT CHANGE**)
- **PackageK:** v0.9.8 (requires F>=2.0.0, **FREE**) | v1.0.0 (conditionally requires F>=2.8.0 if LICENSE_KEY == "VALID_LICENSE_2025", else F>=2.0.0, **$50K ANNUAL LICENSE**)
- **PackageL:** v1.8.5 (requires G>=3.0.0, **CROSS-PLATFORM**) | v2.1.0 (conditionally requires G>=3.5.0 if PLATFORM_TARGET == "windows", else G>=3.0.0, **WINDOWS-ONLY**)
- **PackageM:** v3.0.0 (requires I>=1.0.0 + conditionally H>=4.0.0 if config enables experimental, **MAINTENANCE REQUIRED - CANNOT CHANGE**)

**The Final Solution:**
```
PackageA==1.4.7  # Downgraded to resolve red herring (security trade-off)
PackageF==2.8.9  # Unchanged
PackageG==3.5.2  # Unchanged
PackageH==4.2.6  # Unchanged
PackageI==1.2.3  # Downgraded to resolve compliance conflicts (performance trade-off)
PackageJ==2.0.0  # Unchanged (compliance requirement)
PackageK==0.9.8  # Downgraded to avoid $50k licensing fee (cost trade-off)
PackageL==1.8.5  # Downgraded for Linux compatibility (platform trade-off)
PackageM==3.0.0  # Unchanged (maintenance requirement)
```

**Why this works:**
```
PackageA v1.4.7 → PackageB>=0.9.0,<4.0 (pip selects v0.9.4 for compatibility)
PackageB v0.9.4 → PackageC==0.7.3, PackageD>=2.0 (pip selects v2.3.1)
PackageD v2.3.1 → PackageE==1.2.8
PackageE v1.2.8 → PackageC==0.7.3
PackageF v2.8.9 → PackageC==0.7.3
PackageG v3.5.2 → PackageC==0.7.3 (due to broken env var)
PackageH v4.2.6 → PackageB==0.9.4
PackageI v1.2.3 → PackageD>=1.0.0 (satisfied by v2.3.1)
PackageJ v2.0.0 → PackageE>=1.0.0, PackageC>=0.5.0 (satisfied by v1.2.8, v0.7.3)
PackageK v0.9.8 → PackageF>=2.0.0 (satisfied by v2.8.9)
PackageL v1.8.5 → PackageG>=3.0.0 (satisfied by v3.5.2)
PackageM v3.0.0 → PackageI>=1.0.0 (satisfied by v1.2.3) + PackageH>=4.0.0 (from config, satisfied by v4.2.6)

ALL PATHS CONVERGE ON: Compatible older versions despite all the traps and constraints!
```

## Success Criteria

The agent must:
1. Identify the red herring conflict (A v7.0.3 vs H v4.2.6 over B, plus cross-conflicts between F, G, H)
2. Investigate the deep conflict (A→B→D→E→C vs F→C)
3. Discover PackageG and PackageI's conditional dependency mechanisms
4. Use forensic tools to identify the zero-width spaces in SOLVE_G_CONFLICT and ENABLE_I_OPTIMIZATION
5. Recognize PackageJ's compliance constraints that cannot be violated
6. Trace the complete dependency tree across all 10 packages
7. Accept multiple trade-offs: PackageA==1.4.7 (security) and PackageI==1.2.3 (performance)
8. Successfully install all 10 packages (6 direct + 4 transitive dependencies) with compatible versions

## Testing

The test suite validates:
1. The `requirements.txt` file was modified (PackageA changed from range to 1.4.7, PackageI changed from range to 1.2.3, PackageK changed from range to 0.9.8, PackageL changed from range to 1.8.5)
2. The file still contains exactly 9 package specifications (no additions or deletions)
3. PackageJ remains at version 2.0.0 (compliance requirement)
4. PackageM remains at version 3.0.0 (maintenance requirement)
5. All 13 packages are successfully installed (9 direct + 4 transitive dependencies)
6. All packages exist in site-packages (prevents faking pip output)
7. No dependency conflicts remain (pip can resolve dependencies successfully)

## Skills Tested

This task evaluates the agent's ability to:
1. **Diagnose** - Identify multiple interlocking dependency conflicts from cryptic error messages
2. **Investigate** - Extract and examine package source code (setup.py) to understand behavior
3. **Forensic Analysis** - Use low-level tools (od, cat -A) to discover hidden environmental issues
4. **Trace** - Follow multi-level transitive dependency chains (4 levels deep)
5. **Reason** - Understand that "obvious" conflicts may be red herrings masking deeper problems
6. **Prioritize** - Make difficult trade-offs between security, performance, and compliance constraints
7. **Compliance Awareness** - Recognize regulatory requirements that cannot be violated
8. **Persist** - Continue investigating after initial solutions fail through multiple layers

## Technical Notes

- All packages are served from a local directory (`/packages`) to ensure reproducibility
- Install packages using: `pip install -r requirements.txt --find-links /packages`
- The `pipdeptree` tool is pre-installed for dependency tree visualization
- PackageG, I, K, L's conditional dependencies are evaluated **during package installation**, not runtime
- The zero-width space characters (U+200B) are invisible in most text editors
- **Difficulty: NIGHTMARE** - This task requires forensic investigation skills beyond normal dependency resolution
- **Expected Time:** 45-120 minutes for an experienced developer who recognizes the patterns

## Why This is "Over the Top"

This task is intentionally designed to be **misleadingly complex**:

1. **Red Herring:** The obvious conflict is NOT the real problem
2. **Security FUD:** The security warning creates hesitation to try the correct solution
3. **Performance FUD:** The performance warning adds another layer of complexity
4. **Compliance Constraints:** Regulatory requirements that cannot be violated
5. **Maintenance Constraints:** Custom patches that cannot be changed
6. **Cost Constraints:** Expensive licensing fees to avoid
7. **Platform Constraints:** Windows-only packages in Linux environment
8. **Hidden Layers:** Each "solution" reveals multiple new problems
9. **Multiple Environmental Sabotage:** Four broken environment variables are forensically hidden
10. **Configuration File Traps:** Hidden config files affecting dependencies
11. **Cascading Failures:** Error messages point to multiple packages, obscuring the root cause
12. **Business Constraints:** The critical script creates pressure to keep specific versions
13. **Mental Exhaustion:** Designed to send agents down multiple dead ends before finding the truth

This simulates a real-world "dependency conflict" scenario created by a tired, overworked team making incremental changes without understanding the full dependency graph, compounded by compliance requirements, licensing costs, platform constraints, and environmental issues.
