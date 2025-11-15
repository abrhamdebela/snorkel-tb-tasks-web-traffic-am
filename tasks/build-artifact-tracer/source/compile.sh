#!/bin/bash
set -e

echo "=== Compiling Build Artifact Tracer Binary ==="
echo "Working directory: $(pwd)"
echo "Files present:"
ls -la

echo ""
echo "Step 1: Compiling object files..."
gcc -Wall -O2 -g -c main.c utils.c database.c

echo ""
echo "Step 2: Linking binary..."
gcc -Wall -O2 -g -o target_binary main.o utils.o database.o

echo ""
echo "Step 3: Verifying binary..."
ls -lh target_binary
file target_binary

echo ""
echo "Step 4: Checking for debug symbols..."
readelf -S target_binary | grep -E "debug|symtab" || echo "Warning: No debug sections found"

echo ""
echo "Step 5: Sample symbols..."
nm target_binary | grep -E "(main|initialize|process|cleanup)" | head -10

echo ""
echo "Step 6: Cleanup..."
rm -f *.o

echo ""
echo "=== Build complete! ==="
echo "Binary location: $(pwd)/target_binary"
