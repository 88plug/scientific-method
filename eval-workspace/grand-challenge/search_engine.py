"""Generic stochastic local search engine over coloring certificates.
Parameterized by the methods playbook; verifier = exact fitness."""
import random, sys, time, json
sys.path.insert(0, 'verifiers')
from verify import verify_vdw, verify_schur

def violations_vdw(r, k, coloring):
    """Count of monochromatic k-APs (the SLS objective)."""
    N = len(coloring); v = 0
    for d in range(1, (N-1)//(k-1)+1):
        for a in range(N-(k-1)*d):
            c0 = coloring[a]
            ok = True
            for i in range(1, k):
                if coloring[a+i*d] != c0: ok=False; break
            if ok: v += 1
    return v

def violations_schur(coloring, weak=False):
    N = len(coloring); v=0
    for x in range(1, N+1):
        y0 = x+1 if weak else x
        for y in range(y0, N-x+1):
            z=x+y
            if coloring[x-1]==coloring[y-1]==coloring[z-1]: v+=1
    return v

def sls(N, r, viol_fn, seed=0, max_steps=2_000_000, tabu_len=32, restart_after=200_000, init=None, report=None):
    """Tabu-flavored min-conflicts over colorings of 1..N with r colors."""
    rng = random.Random(seed)
    col = list(init) if init else [rng.randrange(r) for _ in range(N)]
    best = viol_fn(col); best_col = list(col)
    cur = best
    tabu = {}
    steps_since = 0
    for step in range(max_steps):
        if cur == 0: return list(col), 0, step
        i = rng.randrange(N)
        old = col[i]
        # try best alternative color for position i
        cands = []
        for c in range(r):
            if c == old: continue
            if tabu.get((i,c), -1) > step: continue
            col[i] = c
            cands.append((viol_fn(col), c))
        col[i] = old
        if not cands: continue
        cands.sort()
        nv, nc = cands[0]
        if nv <= cur or rng.random() < 0.02:   # accept sideways/up rarely
            tabu[(i, old)] = step + tabu_len
            col[i] = nc; cur = nv
            steps_since = 0 if nv < best else steps_since + 1
            if nv < best: best, best_col = nv, list(col)
        else:
            steps_since += 1
        if steps_since > restart_after:
            col = [rng.randrange(r) for _ in range(N)]; cur = viol_fn(col); steps_since = 0
        if report and step % 50_000 == 0:
            report(step, cur, best)
    return best_col, best, max_steps

if __name__ == '__main__':
    # smoke test: find W(2,4)>34 certificate (W(2,4)=35, so N=34 colorable)
    t0=time.time()
    col, v, steps = sls(34, 2, lambda c: violations_vdw(2,4,c), seed=1, max_steps=300_000)
    ok, d = verify_vdw(2,4,col) if v==0 else (False, f"viol={v}")
    print(f"W(2,4)>34 search: {ok} ({d}) in {steps} steps, {time.time()-t0:.1f}s")
