#!/bin/bash
# Quick test script to verify the nightmare dependency scenario works

set -e

echo "========================================="
echo "Testing Multi-Layered dependency conflict"
echo "========================================="
echo ""

cd "$(dirname "$0")"

echo "Step 1: Building Docker image from scratch..."
docker build --no-cache -t resolve-dep-test .
echo "✓ Image built"
echo ""

echo "Step 2: Verifying initial requirements.txt has 4 packages..."
docker run --rm resolve-dep-test cat /app/requirements.txt
PACKAGE_COUNT=$(docker run --rm resolve-dep-test bash -c "cat /app/requirements.txt | wc -l")
if [ "$PACKAGE_COUNT" -eq 4 ]; then
    echo "✓ Initial requirements.txt has 4 packages"
else
    echo "✗ ERROR: Expected 4 packages, found $PACKAGE_COUNT"
    exit 1
fi
echo ""

echo "Step 3: Checking for zero-width space in SOLVE_G_CONFLICT..."
docker run --rm resolve-dep-test bash -c 'env | grep SOLVE_G_CONFLICT | od -c' | grep -q "342.*200.*213"
if [ $? -eq 0 ]; then
    echo "✓ Zero-width space detected in SOLVE_G_CONFLICT"
else
    echo "✗ WARNING: Zero-width space not found"
fi
echo ""

echo "Step 4: Running solution.sh..."
docker run --rm resolve-dep-test bash /app/solution.sh > /tmp/solution_output.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Solution completed successfully"
else
    echo "✗ ERROR: Solution failed"
    tail -20 /tmp/solution_output.txt
    exit 1
fi
echo ""

echo "Step 5: Verifying final requirements.txt still has 4 packages..."
docker run --rm resolve-dep-test bash -c "bash /app/solution.sh >/dev/null 2>&1 && cat /app/requirements.txt"
FINAL_COUNT=$(docker run --rm resolve-dep-test bash -c "bash /app/solution.sh >/dev/null 2>&1 && cat /app/requirements.txt | wc -l")
if [ "$FINAL_COUNT" -eq 4 ]; then
    echo "✓ Final requirements.txt has 4 packages"
else
    echo "✗ ERROR: Expected 4 packages in final requirements.txt, found $FINAL_COUNT"
    exit 1
fi
echo ""

echo "Step 6: Running pytest tests..."
docker run --rm resolve-dep-test bash -c "bash /app/solution.sh >/dev/null 2>&1 && pytest /app/tests/ -v"
if [ $? -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed (see output above)"
    exit 1
fi
echo ""

echo "========================================="
echo "✓ ALL CHECKS PASSED!"
echo "========================================="
echo ""
echo "The multi-layered dependency conflict task is working correctly!"
