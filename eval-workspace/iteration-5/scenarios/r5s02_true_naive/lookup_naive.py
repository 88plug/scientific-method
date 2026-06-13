import sys,time
def find(xs,q):
    for i,x in enumerate(xs):
        if x==q: return i
    return -1
if __name__=="__main__":
    import random
    n=int(sys.argv[1]) if len(sys.argv)>1 else 50
    xs=list(range(n)); random.seed(1)
    qs=[random.randrange(n) for _ in range(200000)]
    t0=time.perf_counter()
    for q in qs: find(xs,q)
    print(f"naive n={n}: {time.perf_counter()-t0:.3f}s")
