#!/bin/bash
# official benchmark
echo "=== A ==="
time (python3 impl_a.py --build-index && python3 impl_a.py --query)
echo "=== B ==="
time python3 impl_b.py
