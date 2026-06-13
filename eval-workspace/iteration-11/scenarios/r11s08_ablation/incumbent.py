import sys, time
# incumbent: per-query set intersection over a tiny inverted index
def build(qs):
    idx={}
    for i,q in enumerate(qs):
        for t in q.split(): idx.setdefault(t,set()).add(i)
    return idx
if __name__=='__main__':
    qs=[l.strip() for l in open('queries.txt')]
    idx=build(qs)
    t0=time.perf_counter()
    total=0
    for q in qs[:20000]:
        terms=q.split()
        res=set(idx.get(terms[0],set()))
        for t in terms[1:]: res &= idx[t]
        total+=len(res)
    print(f"checksum={total} time={time.perf_counter()-t0:.3f}s")
