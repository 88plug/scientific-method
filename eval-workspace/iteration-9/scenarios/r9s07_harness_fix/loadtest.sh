#!/bin/bash
# usage: loadtest.sh <impl1.py> <impl2.py>
r1=$(python3 "$1"); sleep 0.2
r2=$(python3 "$2")
echo "target1($1): $r1 req/s"
echo "target2($2): $r2 req/s"
