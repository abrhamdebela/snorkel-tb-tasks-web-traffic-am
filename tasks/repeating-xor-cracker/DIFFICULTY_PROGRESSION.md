# Difficulty Progression Tracking for repeating-xor-cracker

This document tracks the iterative difficulty increases applied to the repeating-xor-cracker task. Each level builds upon the previous, adding new challenging dimensions while maintaining solvability.

## Level Summary

| Level | Description | Messages | Key Length | Key Complexity | Content Type | Special Features | Oracle Result | Date |
|-------|-------------|----------|------------|----------------|--------------|------------------|---------------|------|
| 1 (Archived) | Baseline data set | 10 | 24 bytes | Mixed ASCII/non-printable | English-like technical | None | ✅ PASS | 2025-11-11 |
| 2 (Archived) | Reduced corpus | 8 | 24 bytes | Mixed ASCII/non-printable | English-like technical | Fewer samples | ✅ PASS | 2025-11-12 |
| 3 (Current) | Longer key | 7 | 32 bytes | More non-printable | English-like technical | Longer key | ✅ PASS | 2025-11-12 |
| 4 | Non-English content | 8 | 32 bytes | More non-printable | Mixed (hex/base64/binary) | Binary-like patterns | ⏳ Pending | 2025-11-11 |
| 5 | Variable length | 8 | 32 bytes | More non-printable | Mixed | Short + long messages | ⏳ Pending | 2025-11-11 |
| 6 | Red herrings | 7 | 32 bytes | More non-printable | Mixed | Corrupted messages | ⏳ Pending | 2025-11-11 |
| 7 | Maximum difficulty | 5 | 40 bytes | Maximum non-printable | Binary/encoded | All features combined | ⏳ Pending | 2025-11-11 |

## Detailed Level Documentation

### Level 1: Baseline (Archived)

**Configuration:**
- Messages: 10
- Key: 24 bytes `[0x54, 0x45, 0x52, 0x4d, 0x49, 0x4e, 0x41, 0x4c, 0x42, 0x45, 0x4e, 0x43, 0x48, 0x7F, 0xA3, 0x5C, 0x91, 0xB2, 0xC4, 0xD5, 0xE6, 0xF7, 0x8A, 0x9B]`
- Key printable ratio: ~58% (14/24 bytes printable)
- Average message length: ~85 bytes
- Message types: Technical English text (errors, code, JSON, URLs, logs, etc.)
- Target: message1.hex (longest message)

**Statistics:**
- Total corpus size: ~850 bytes
- Key cycles per message: 1-4 cycles
- Character distribution: Mostly ASCII printable, some symbols

**Oracle Test Results:**
- Status: ✅ PASS (archived)
- Test execution time: ~42s
- All tests passing: Yes

**Rationale:**
Baseline difficulty with sufficient data for statistical analysis. Good mix of message types provides diverse character distributions for frequency analysis.

---

### Level 2: Reduced Corpus (Archived)

**Changes from Level 1:**
- Reduced messages from 10 to 8
- Removed 2 messages (message9, message10) to reduce statistical data
- Target: message1.hex (kept longer target for oracle validation)

**Configuration:**
- Messages: 8
- Key: 24 bytes (unchanged)
- Key printable ratio: ~58%
- Average message length: ~85 bytes
- Message types: Technical English text

**Statistics:**
- Total corpus size: ~680 bytes (20% reduction)
- Key cycles per message: 1-4 cycles
- Character distribution: Mostly ASCII printable

**Oracle Test Results:**
- Status: ✅ PASS (archived)
- Test execution time: ~48 seconds
- All tests passing: Yes
- Notes: Additional technical-word scoring and debug logging added to oracle solution to improve key-byte recovery with smaller corpora.

**Rationale:**
Less statistical data makes frequency analysis harder. Fewer samples per key position reduces confidence in key recovery.

**Implementation Notes:**
- Removed messages: `message9.hex`, `message10.hex`
- Target: `message1.hex` (longest message, kept for oracle validation)
- Oracle solution enhanced (technical word scoring + debugging) to remain reliable with reduced statistical data.

---

### Level 3: Longer, More Complex Key (Current State)

**Changes from Level 2:**
- Increased key length from 24 to 32 bytes
- Added more non-printable bytes (0x03, 0x1D, 0x80, 0xF1)
- Reduced corpus slightly (7 messages) to keep per-position statistics tight

**Configuration:**
- Messages: 7
- Key: 32 bytes (new key with additional non-printable bytes)
- Key printable ratio: ~41% (13/32 bytes printable)
- Average message length: ~85 bytes
- Message types: Technical English text

**Statistics:**
- Total corpus size: ~595 bytes
- Key cycles per message: typically 1-2 cycles (longer key, fewer repeats)
- Character distribution: Mostly ASCII printable with technical vocabulary

**Oracle Test Results:**
- Status: ✅ PASS (2025-11-12)
- Test execution time: ~57 seconds
- All tests passing: Yes

**Rationale:**
Longer keys make Hamming distance analysis more computationally expensive. More non-printable bytes reduce patterns that could be exploited.

**Implementation Notes:**
- Key updated to 32-byte sequence `[0x54, 0x45, ..., 0x6C]`
- Corpus trimmed to first seven baseline messages to emphasize longer key detection
- Target remains `message1.hex` to preserve longest/plaintext requirement
- Strengthened `score_text` with hybrid word-frequency heuristics
- Added cached per-position candidates and beam-search refinement to `recover_key`

---

### Level 4: Non-English Content

**Changes from Level 3:**
- Replaced some messages with non-English content:
  - Hex dumps (e.g., "0x4a3f2c1b...")
  - Base64 encoded strings
  - IPv6 addresses and MAC addresses
  - Escaped unicode sequences
  - File format headers (PNG, PDF signatures)
- Keep 2-3 English messages for context

**Configuration:**
- Messages: 7
- Key: 32 bytes
- Key printable ratio: ~40%
- Average message length: ~85 bytes
- Message types: Mixed (2-3 English, 4-5 binary-like)

**Statistics:**
- Total corpus size: ~595 bytes
- Key cycles per message: 1-3 cycles
- Character distribution: Mixed (lower letter frequency)

**Oracle Test Results:**
- Status: ⏳ Pending
- Test execution time: TBD
- All tests passing: TBD

**Rationale:**
Frequency analysis becomes unreliable with non-alphabetic content. Requires more sophisticated scoring that doesn't rely solely on English letter frequencies.

**Implementation Notes:**
- Update scoring function to handle non-English content
- May need to adjust test expectations for readability checks

---

### Level 5: Variable Length with Noise

**Changes from Level 4:**
- Add very short messages (15-30 bytes) - less than 1 key cycle
- Add very long messages (300+ bytes)
- Include messages with unusual character distributions (all numbers, all symbols)

**Configuration:**
- Messages: 7
- Key: 32 bytes
- Key printable ratio: ~40%
- Message lengths: 15-30 bytes (short), 80-120 bytes (medium), 300+ bytes (long)
- Message types: Mixed content with extreme distributions

**Statistics:**
- Total corpus size: ~800 bytes (increased due to long messages)
- Key cycles per message: 0-1 cycles (short), 2-3 cycles (medium), 9+ cycles (long)
- Character distribution: Highly variable

**Oracle Test Results:**
- Status: ⏳ Pending
- Test execution time: TBD
- All tests passing: TBD

**Rationale:**
Short messages provide minimal data per key position. Length variance makes Hamming distance less reliable. Unusual distributions break frequency assumptions.

**Implementation Notes:**
- Short messages may have insufficient data for some key positions
- Long messages provide more data but may have different patterns
- Need robust handling of edge cases

---

### Level 6: Red Herrings

**Changes from Level 5:**
- Add 2-3 "corrupted" messages encrypted with slightly different key (1-2 bytes different)
- Add misleading patterns (repeated sections within messages)
- Include one message that looks like it could be plaintext of another
- Update tests to only validate uncorrupted messages

**Configuration:**
- Messages: 7 (5 valid + 2 corrupted)
- Key: 32 bytes (main key)
- Corrupted key: 32 bytes (1-2 bytes different)
- Key printable ratio: ~40%
- Message lengths: Variable
- Message types: Mixed with decoy patterns

**Statistics:**
- Total corpus size: ~800 bytes
- Valid messages: 5
- Corrupted messages: 2
- Key cycles per message: Variable

**Oracle Test Results:**
- Status: ⏳ Pending
- Test execution time: TBD
- All tests passing: TBD

**Rationale:**
Forces agents to validate key consistency across corpus. Can't assume all messages use identical keys. Requires filtering/validation logic.

**Implementation Notes:**
- Tests must identify and skip corrupted messages
- Need to document which messages are corrupted
- Agent must detect inconsistencies

---

### Level 7: Maximum Difficulty

**Changes from Level 6:**
- Reduce to 5 messages total
- 40-byte key with maximum non-printable bytes
- Mix of very short (20 bytes) and very long (500 bytes) messages
- Content: Compressed data representations, encoded binary, minimal patterns
- 1 corrupted message with different key
- Target: Shortest message with least English-like content

**Configuration:**
- Messages: 5 (4 valid + 1 corrupted)
- Key: 40 bytes (maximum complexity)
- Key printable ratio: ~30% (12/40 bytes printable)
- Message lengths: 20 bytes (short), 80-120 bytes (medium), 500 bytes (long)
- Message types: Binary/encoded with minimal English patterns

**Statistics:**
- Total corpus size: ~750 bytes
- Valid messages: 4
- Corrupted messages: 1
- Key cycles per message: 0-1 (short), 2-3 (medium), 12+ (long)
- Character distribution: Minimal English patterns

**Oracle Test Results:**
- Status: ⏳ Pending
- Test execution time: TBD
- All tests passing: TBD

**Rationale:**
Combines all difficulty dimensions. Requires robust algorithms and careful validation. Tests maximum capabilities of cracking algorithms.

**Implementation Notes:**
- Most challenging configuration
- May require algorithm refinements
- Target is intentionally difficult (short, non-English)

---

## Oracle Solution Performance Analysis

### Performance Metrics by Level

| Level | Execution Time | Memory Usage | Key Recovery Accuracy | Notes |
|-------|----------------|--------------|----------------------|-------|
| 1 | TBD | TBD | 100% | Baseline |
| 2 | TBD | TBD | TBD | Reduced data |
| 3 | TBD | TBD | TBD | Longer key |
| 4 | TBD | TBD | TBD | Non-English |
| 5 | TBD | TBD | TBD | Variable length |
| 6 | TBD | TBD | TBD | Red herrings |
| 7 | TBD | TBD | TBD | Maximum difficulty |

## Algorithm Requirements by Level

### Level 1-2: Basic Requirements
- Hamming distance for key length estimation
- Frequency analysis for key recovery
- Basic English scoring

### Level 3: Enhanced Key Length Detection
- Extended Hamming distance analysis
- More candidate key lengths to test
- Iterative refinement

### Level 4: Advanced Scoring
- Non-English content handling
- Binary pattern recognition
- Flexible character distribution scoring

### Level 5: Robust Length Handling
- Short message handling (insufficient data)
- Long message optimization
- Variable distribution scoring

### Level 6: Validation & Filtering
- Key consistency checking
- Corrupted message detection
- Pattern validation

### Level 7: Maximum Robustness
- All previous requirements
- Sparse data handling
- Complex key recovery
- Edge case management

## Recommendations

### Sweet Spot Identification
- **TBD**: Will identify the hardest solvable level after all tests complete

### Potential Oracle Failures
- **TBD**: Document any levels where oracle fails and why

### Agent Difficulty Assessment
- **TBD**: Estimate which levels will challenge different agent capabilities

## Implementation History

- **2025-11-11**: Level 1 baseline established (10 messages, 24-byte key)
- **2025-11-11**: Level 2 implemented - Reduced to 8 messages (oracle failing, needs investigation)
- **2025-11-11**: Level 3 implemented - Increased key to 32 bytes with more non-printable bytes
- **2025-11-11**: Level 4 implemented - Added non-English content (hex dumps, base64, binary patterns)
- **2025-11-11**: Level 5 implemented - Variable length messages (very short and very long)
- **2025-11-11**: Level 6 implemented - Added corrupted messages with different keys (2 corrupted out of 7 total)
- **2025-11-11**: Level 7 implemented - Maximum difficulty (5 messages, 40-byte key, all features combined)

## Current Status

**All 7 levels have been implemented and data generated.**

**Next Steps:**
1. Run oracle validation for each level (Levels 3-7)
2. Document oracle results in this file
3. Identify which level causes first oracle failure (if any)
4. Adjust difficulty if needed to ensure solvability
5. Update task.yaml difficulty ratings for each level variant

**Note:** Level 2 is currently failing oracle validation. This may indicate:
- Oracle solution needs refinement for reduced corpus
- Level 2 difficulty may need adjustment (e.g., keep 9 messages instead of 8)
- Further investigation needed into oracle solution algorithm robustness

