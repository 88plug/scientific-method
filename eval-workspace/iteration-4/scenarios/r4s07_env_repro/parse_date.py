import sys, time, os
from datetime import datetime
# parses epoch of "YYYY-MM-DD HH:MM" in LOCAL time then converts
s="2026-03-08 02:30"   # report row that crashes "sometimes"
try:
    t=time.mktime(time.strptime(s,"%Y-%m-%d %H:%M"))
    print(f"ok epoch={int(t)}")
except Exception as e:
    print(f"CRASH: {e}"); sys.exit(1)
