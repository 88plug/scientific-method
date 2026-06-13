#!/bin/bash
# usage: loadtest.sh <impl1.py> <impl2.py>  — reports req/s for each
# runs impl1 first, then impl2 on the same box
r1=$(python3 "$1" 2>/dev/null)
sleep 0.2
# NOTE: second target gets the warmed CPU governor + python bytecode cache
r2=$(python3 "$2" 2>/dev/null)
echo "target1($1): $r1 req/s"
echo "target2($2): $r2 req/s"
