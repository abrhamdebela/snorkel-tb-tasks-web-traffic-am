#!/usr/bin/env python3
"""Generate binary data files in proprietary format."""

import struct
import os

# Format specification (hidden from agent):
# - Magic bytes: 0x44 0x46 (DF = Data Format)
# - Version: 1 byte (0x01)
# - Record count: 2 bytes (little-endian uint16)
#
# Each record:
# - ID: 4 bytes (little-endian uint32)
# - Timestamp: 8 bytes (little-endian uint64)
# - Category length: 1 byte
# - Category: N bytes (UTF-8 string)
# - Value: 4 bytes (little-endian float32)
# - Flags: 1 byte bitfield
#   - Bit 0: ACTIVE
#   - Bit 1: VERIFIED
#   - Bit 2: CRITICAL
#   - Bit 3: ARCHIVED


def encode_record(record_id, timestamp, category, value, flags):
    """Encode a single record to bytes."""
    data = b""
    data += struct.pack("<I", record_id)
    data += struct.pack("<Q", timestamp)
    cat_bytes = category.encode("utf-8")
    data += struct.pack("B", len(cat_bytes))
    data += cat_bytes
    data += struct.pack("<f", value)

    # Convert flag list to bitfield
    flag_byte = 0
    if "ACTIVE" in flags:
        flag_byte |= 0x01
    if "VERIFIED" in flags:
        flag_byte |= 0x02
    if "CRITICAL" in flags:
        flag_byte |= 0x04
    if "ARCHIVED" in flags:
        flag_byte |= 0x08

    data += struct.pack("B", flag_byte)
    return data


def create_file(filename, records):
    """Create a binary file with given records."""
    with open(filename, "wb") as f:
        # Header
        f.write(b"\x44\x46")  # Magic
        f.write(b"\x01")  # Version
        f.write(struct.pack("<H", len(records)))

        # Records
        for rec in records:
            f.write(
                encode_record(
                    rec["id"],
                    rec["timestamp"],
                    rec["category"],
                    rec["value"],
                    rec["flags"],
                )
            )


# Sample data
samples = [
    {
        "filename": "sample1.dat",
        "records": [
            {
                "id": 1001,
                "timestamp": 1704067200,
                "category": "sensor",
                "value": 23.5,
                "flags": ["ACTIVE", "VERIFIED"],
            },
            {
                "id": 1002,
                "timestamp": 1704070800,
                "category": "actuator",
                "value": 100.0,
                "flags": ["ACTIVE"],
            },
        ],
    },
    {
        "filename": "sample2.dat",
        "records": [
            {
                "id": 2001,
                "timestamp": 1704153600,
                "category": "temperature",
                "value": 72.3,
                "flags": ["ACTIVE", "VERIFIED", "CRITICAL"],
            },
            {
                "id": 2002,
                "timestamp": 1704157200,
                "category": "pressure",
                "value": 14.7,
                "flags": ["VERIFIED"],
            },
            {
                "id": 2003,
                "timestamp": 1704160800,
                "category": "flow",
                "value": 5.2,
                "flags": ["ACTIVE", "ARCHIVED"],
            },
        ],
    },
    {
        "filename": "sample3.dat",
        "records": [
            {
                "id": 3001,
                "timestamp": 1704240000,
                "category": "voltage",
                "value": 12.1,
                "flags": ["ACTIVE", "VERIFIED"],
            },
        ],
    },
]

test_data = {
    "filename": "test.dat",
    "records": [
        {
            "id": 5001,
            "timestamp": 1704326400,
            "category": "humidity",
            "value": 45.8,
            "flags": ["ACTIVE", "VERIFIED"],
        },
        {
            "id": 5002,
            "timestamp": 1704330000,
            "category": "light",
            "value": 850.0,
            "flags": ["ACTIVE", "CRITICAL"],
        },
        {
            "id": 5003,
            "timestamp": 1704333600,
            "category": "motion",
            "value": 1.0,
            "flags": ["VERIFIED", "ARCHIVED"],
        },
        {
            "id": 5004,
            "timestamp": 1704337200,
            "category": "sound",
            "value": 65.3,
            "flags": ["ACTIVE"],
        },
    ],
}

os.makedirs("data/samples", exist_ok=True)

for sample in samples:
    create_file(f"data/samples/{sample['filename']}", sample["records"])

create_file("data/test.dat", test_data["records"])

print("Generated all data files")
