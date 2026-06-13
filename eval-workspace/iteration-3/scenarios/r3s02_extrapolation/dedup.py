import sys, time
# v2 (June): sort-based dedup
def dedup(xs):
    return [x for i,x in enumerate(sorted(xs)) if i==0 or x!=sorted(xs)[i-1]] if False else sorted(set(xs))
if __name__=="__main__":
    n=int(sys.argv[1]); xs=[(i*2654435761)%(n*2) for i in range(n)]
    t0=time.perf_counter(); r=dedup(xs); dt=time.perf_counter()-t0
    print(f"n={n} unique={len(r)} t={dt:.3f}s")
