# Task Comparison: reverse-engineer-data-format vs reverse-engineer-protocol

This document explains the differences between the two binary reverse-engineering tasks and why the "protocol" version is more challenging.

## Overview

Both tasks require reverse-engineering a proprietary binary format, but the "protocol" version adds four key challenges that test deeper reverse-engineering skills without being unfair tricks.

---

## Difference 1: Header Structure - Record Count

### Data-Format (Easier)
```
[44 46][01][02 00]
 Magic  Ver RecCount (little-endian uint16)

Total: 5 bytes
Record count: EXPLICIT (tells you how many records to read)
```

### Protocol (Harder)
```
[44 46][01][00 00]
 Magic  Ver Padding (alignment bytes)

Total: 5 bytes
Record count: NOT PROVIDED (must parse until EOF)
```

**Impact**: Protocol version requires proper EOF handling and can't pre-allocate arrays. Tests boundary detection and robust parsing.

**Why Fair**: Real network protocols often don't include record counts - this is common in streaming protocols.

---

## Difference 2: Record Field Ordering

### Data-Format (Easier)
```
[ID][Timestamp][CatLen][Category][Value][Flags]
                                  ^^^^^ ^^^^^
                                  Value comes BEFORE Flags
```

### Protocol (Harder)
```
[ID][Timestamp][CatLen][Category][Flags][Value]
                                  ^^^^^ ^^^^^
                                  Flags comes BEFORE Value
```

**Impact**: You can't assume standard field ordering - must reverse-engineer the actual order through analysis.

**Why Fair**: Different protocols order fields differently. This tests whether engineers verify assumptions vs. guessing.

---

## Difference 3: ID Field Endianness (Mixed Endianness)

### Data-Format (Easier)
```
ID: [e9 03 00 00] = 0x000003e9 (little-endian) = 1001
     ^^^^^^^^^^^
     All fields use little-endian (consistent)
```

### Protocol (Harder)
```
ID: [00 00 03 e9] = 0x000003e9 (big-endian) = 1001
     ^^^^^^^^^^^
     ID uses big-endian, but timestamp/value use little-endian
```

**Impact**: This is **mixed endianness** - must test both byte orders for each field type.

**Why Fair**: Big-endian (network byte order) is standard in real network protocols like TCP/IP. Mixed endianness appears in protocols that evolved over time or bridge different systems.

---

## Difference 4: Alignment Padding

### Data-Format (Easier)
- No padding bytes
- Header is: Magic (2) + Version (1) + RecordCount (2) = 5 bytes

### Protocol (Harder)
- Has 2-byte padding after version byte
- Header is: Magic (2) + Version (1) + Padding (2) = 5 bytes

**Impact**: Must identify and skip non-data bytes. Tests recognition of alignment patterns.

**Why Fair**: Real binary formats use alignment padding for performance (e.g., aligning to 4-byte or 8-byte boundaries).

---

## Fields That Are The Same

| Field | Both Versions |
|-------|---------------|
| Magic bytes | `44 46` ("DF") |
| Version | `01` |
| Timestamp | 8 bytes, little-endian uint64 |
| Category Length | 1 byte |
| Category | UTF-8 string (length-prefixed) |
| Value | 4 bytes, little-endian float32 |
| Flags | 1 byte bitfield (ACTIVE=0x01, VERIFIED=0x02, CRITICAL=0x04, ARCHIVED=0x08) |

---

## Summary Table

| Aspect | Data-Format (Easier) | Protocol (Harder) |
|--------|---------------------|-------------------|
| **Record Count** | ✅ Provided in header | ❌ Must parse until EOF |
| **Header Padding** | ❌ No padding | ✅ 2-byte padding |
| **ID Endianness** | Little-endian | **Big-endian** ⚠️ |
| **Field Order** | Value → Flags | **Flags → Value** ⚠️ |
| **Mixed Endianness** | ❌ No (all little-endian) | ✅ Yes (ID is big-endian) |
| **Difficulty** | Hard | **Harder** |
| **Expert Time Estimate** | 45 min | 60 min |
| **Junior Time Estimate** | 90 min | 120 min |

---

## Why These Changes Are Fair

All four changes require **genuine reverse-engineering analysis** without being tricks or gotchas:

1. **No Record Count**: Common in streaming protocols, tests EOF handling
2. **Big-Endian ID**: Standard in network protocols (network byte order)
3. **Padding Bytes**: Used for memory alignment in real formats
4. **Field Reordering**: Different protocols have different conventions

An experienced engineer should identify these through:
- Systematic testing of byte order hypotheses
- Comparing headers across multiple sample files
- Validating field boundaries against known values (strings, floats)
- Testing parsing until EOF vs. fixed counts

None of these involve:
- ❌ Corrupted data or fake patterns
- ❌ Encryption/obfuscation
- ❌ Misleading magic bytes
- ❌ Counter-intuitive data that seems invalid

The protocol version simply requires more thorough analysis and tests deeper understanding of binary formats and network protocols.
