#!/usr/bin/env python3
"""Generate heterogeneous input data files for streaming CLI task."""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)

# Create input directory
input_dir = Path("/app/input")
input_dir.mkdir(exist_ok=True)

# Generate schema.json
schema = {
    "columns": {
        "id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "age": {"type": "integer", "required": False},
        "salary": {"type": "float", "required": False},
        "is_active": {"type": "boolean", "required": False},
        "created_at": {"type": "datetime", "required": False},
        "category": {"type": "string", "required": False}
    },
    "composite_key": ["id", "name"]
}

with open("/app/schema.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2)

print("Generated schema.json")

# Generate CSV file (UTF-8, comma-delimited, with BOM)
csv_data = []
for i in range(1, 101):
    csv_data.append({
        "id": str(i),
        "name": f"User {i}",
        "age": str(random.randint(20, 65)),
        "salary": f"{random.uniform(30000, 150000):.2f}",
        "is_active": random.choice(["true", "false", "1", "0", "yes", "no"]),
        "created_at": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
        "category": random.choice(["A", "B", "C", ""])
    })

# Write with BOM
with open(input_dir / "data.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "salary", "is_active", "created_at", "category"])
    writer.writeheader()
    writer.writerows(csv_data)

print("Generated data.csv (UTF-8 with BOM)")

# Generate TSV file (Latin-1, tab-delimited, with some malformed rows)
tsv_data = []
for i in range(101, 201):
    row = {
        "id": str(i),
        "name": f"Person {i}",
        "age": str(random.randint(18, 70)) if random.random() > 0.1 else "",  # 10% missing
        "salary": f"{random.uniform(25000, 200000):.2f}" if random.random() > 0.15 else "",  # 15% missing
        "is_active": random.choice(["True", "False", "TRUE", "FALSE", ""]),
        "created_at": (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y/%m/%d %H:%M") if random.random() > 0.05 else "",
        "category": random.choice(["X", "Y", "Z", ""])
    }
    tsv_data.append(row)

# Write TSV with Latin-1 encoding
with open(input_dir / "data.tsv", "w", encoding="latin-1", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "salary", "is_active", "created_at", "category"], delimiter="\t")
    writer.writeheader()
    writer.writerows(tsv_data)
    # Add a malformed row with embedded newline
    f.write('202\t"Person\nwith newline"\t30\t50000.0\ttrue\t2024-01-01 12:00:00\tA\n')

print("Generated data.tsv (Latin-1, tab-delimited)")

# Generate JSON file (UTF-8, with some outliers and duplicates)
json_data = []
for i in range(201, 301):
    # Add some outliers
    salary = random.uniform(30000, 150000)
    if random.random() < 0.05:  # 5% outliers
        salary = random.uniform(1000000, 5000000)
    
    json_data.append({
        "id": i,
        "name": f"Entity {i}",
        "age": random.randint(25, 60) if random.random() > 0.1 else None,
        "salary": salary,
        "is_active": random.choice([True, False, "true", "false", 1, 0]),
        "created_at": (datetime.now() - timedelta(days=random.randint(0, 1095))).isoformat(),
        "category": random.choice(["P", "Q", "R", None])
    })

# Add some duplicates (same composite key)
json_data.append(json_data[0].copy())  # Duplicate of first entry

with open(input_dir / "data.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, default=str)

print("Generated data.json (UTF-8)")

print("All input data files generated successfully")

