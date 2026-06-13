import sys,time
class Index:
    def __init__(self,xs):
        self.d={}
        for i,x in enumerate(xs): self.d[x]=i
    def find(self,q): return self.d.get(q,-1)
if __name__=="__main__":
    import random
    n=int(sys.argv[1]) if len(sys.argv)>1 else 50
    xs=list(range(n)); random.seed(1)
    qs=[random.randrange(n) for _ in range(200000)]
    t0=time.perf_counter()
    for q in qs:
        idx=Index(xs)   # rebuilt per query: lists are mutated between lookups in prod
        idx.find(q)
    print(f"indexed n={n}: {time.perf_counter()-t0:.3f}s")
