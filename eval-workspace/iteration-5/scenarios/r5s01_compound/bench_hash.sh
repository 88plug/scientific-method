#!/bin/bash
# official numbers for WALLS.md: total time on the 400MB corpus
python3 hasher.py corpus.bin | grep -o "total=.*"
