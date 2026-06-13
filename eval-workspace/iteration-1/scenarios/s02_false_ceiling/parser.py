#!/usr/bin/env python3
"""CSV record parser. --no-validate skips per-row schema validation (regex)."""
import sys, re, time, argparse
ROW_RE = re.compile(r'^(\d+),([A-Za-z ]+),(\d{4}-\d{2}-\d{2}),([0-9.]+)$')
def parse(path, validate=True):
    n=0
    with open(path) as f:
        for line in f:
            if validate:
                m=ROW_RE.match(line.strip())
                if not m: continue
                rec=(int(m.group(1)),m.group(2),m.group(3),float(m.group(4)))
            else:
                p=line.rstrip('\n').split(',')
                if len(p)!=4: continue
                rec=(int(p[0]),p[1],p[2],float(p[3]))
            n+=1
    return n
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('--no-validate',action='store_true')
    a=ap.parse_args()
    t0=time.perf_counter(); n=parse(a.file, validate=not a.no_validate); dt=time.perf_counter()-t0
    print(f"{n} rows in {dt:.3f}s = {n/dt:,.0f} rows/s")
