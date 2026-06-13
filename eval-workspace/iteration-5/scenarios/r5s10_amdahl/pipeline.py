import time, sys
def fetch(n):      time.sleep(0.9)   # network-bound: 0.9s
def parse(n):
    t0=time.perf_counter()
    s=0
    for i in range(n//2): s+=i%7      # the "optimized" stage
    return time.perf_counter()-t0
def parse_old(n):
    t0=time.perf_counter()
    s=0
    for i in range(n): s+=i%7
    return time.perf_counter()-t0
def store(n):      time.sleep(0.6)
if __name__=='__main__':
    n=3_000_000
    mode=sys.argv[1] if len(sys.argv)>1 else 'new'
    t0=time.perf_counter()
    fetch(n)
    pt=parse(n) if mode=='new' else parse_old(n)
    store(n)
    print(f"mode={mode} parse={pt:.3f}s end_to_end={time.perf_counter()-t0:.3f}s")
