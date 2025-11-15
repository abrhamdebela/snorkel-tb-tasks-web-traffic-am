# Build Artifact Tracer

## Overview
This task challenges agents to **reverse engineer** a compiled binary and reconstruct its source code origins through static analysis and disassembly techniques - **without access to the original source code**.

## Difficulty: Hard
This is a true reverse engineering challenge. The source code is kept in the repository for reference but is **NOT included in the Docker container**. Agents must reconstruct the source file structure purely from binary analysis.

## Task Description
Given only a compiled binary and optional build metadata, the agent must:
1. Extract symbols, strings, and debug information from the binary
2. Analyze DWARF debug data (if present) to extract source file references
3. Infer source file structure from symbol naming patterns
4. Reconstruct likely source file names and their contents
5. Calculate confidence scores for each identified/inferred source file

## Directory Structure
```
build-artifact-tracer/
├── task.yaml              # Task configuration
├── Dockerfile             # Container definition (source NOT copied)
├── docker-compose.yaml    # Docker compose configuration
├── run-tests.sh          # Test execution script
├── solution.sh           # Reference solution using reverse engineering
├── binary/               # Compiled binary artifacts (AVAILABLE in container)
│   └── target_binary     # Sample compiled binary to analyze
├── source/               # Source code files (NOT in container - for reference only)
│   ├── main.c           # Main program file (must be inferred)
│   ├── utils.c          # Utility functions (must be inferred)
│   ├── utils.h          # Utility headers
│   ├── database.c       # Database functions (must be inferred)
│   ├── database.h       # Database headers
│   ├── helper.c         # Decoy file (not in binary - tests inference)
│   └── Makefile         # Build configuration
├── data/                # Metadata (AVAILABLE in container)
│   └── build_info.json  # Build metadata (compiler, flags, etc.)
└── tests/               # Test files
    └── test_outputs.py  # Pytest test suite
```

## Inputs (Available in Container)
- `/app/binary/target_binary` - Compiled executable to reverse engineer
- `/app/data/build_info.json` - Optional build metadata
- **NO SOURCE CODE** - Must be reconstructed from binary analysis

## Outputs Required
- `/app/output/trace_report.json` - Reverse engineering report with:
  - `binary_info`: Architecture, compiler (detected), stripped status
  - `source_matches`: Array of reconstructed/inferred source files with confidence scores
  - `top_match`: Most likely primary source file
  - `total_symbols_analyzed`: Count of extracted symbols

- `/app/output/symbols.txt` - All extracted symbols (sorted alphabetically) with type prefixes:
  - `F:` for functions
  - `D:` for data symbols
  - `U:` for undefined/external symbols

## Reverse Engineering Approach
Agents should use tools like:
- `nm` - Extract symbol tables
- `objdump` - Disassemble and extract DWARF debug information
- `readelf` - Read ELF headers and debug sections
- `strings` - Extract string literals
- `file` - Identify binary type and architecture

## Confidence Scoring
Since source files must be reconstructed, confidence should be based on:
- **Debug information presence** (50%) - If file paths are in DWARF data
- **Symbol attribution** (30%) - Number of symbols linked to that file
- **String evidence** (20%) - String literals suggesting file names/modules

## Test Coverage
The pytest suite validates:
- Output file existence and structure
- Binary metadata extraction (architecture, compiler)
- Symbol extraction completeness
- Source file reconstruction (must identify C/C++ files)
- Confidence score validity (0.0-1.0 range)
- Alphabetical sorting of symbols
- UTF-8 encoding and newlines
- Input file immutability

## Challenge Aspects
1. **No source code access** - Must infer everything from binary
2. **Debug symbol extraction** - Parse DWARF data to find file references
3. **Pattern recognition** - Infer modules from symbol naming conventions
4. **Confidence estimation** - Rank reconstructed files by likelihood

## Building the Binary (For Maintainers)
The binary is pre-built with debug symbols (not stripped):
```bash
cd source/
gcc -Wall -O2 -c main.c utils.c database.c
gcc -Wall -O2 -o target_binary main.o utils.o database.o
mv target_binary ../binary/
```

## Notes
- The binary is compiled with debug symbols to make the challenge feasible
- Agents must extract file paths from DWARF debug information
- Symbol naming patterns can help infer module organization
- The `helper.c` file is NOT in the binary - tests ability to avoid false positives
- Standard reverse engineering tools (`binutils`, `file`) are provided in the container
