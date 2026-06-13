#!/bin/bash
# W3 probe (as run for the ledger entry above)
python3 scan.py --mode map   data.bin   # NB: flag value
python3 scan.py --mode buf data.bin
