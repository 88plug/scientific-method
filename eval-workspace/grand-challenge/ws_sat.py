"""Weak-Schur SAT attack: is [1,N] partitionable into r weakly-sum-free sets?
weak sum-free: no monochromatic x+y=z with x<y, z=x+y<=N (distinct x,y,z).
If SAT for N > current record, the model IS a new-record certificate.
Direct, verifier-backed, no envelope."""
import sys, time, json
sys.path.insert(0,'verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def solve(N, r, time_limit=None, seed_assign=None):
    vp = IDPool()
    def V(i,c): return vp.id(('x',i,c))
    cl = []
    # exactly-one color per integer
    for i in range(1, N+1):
        lits = [V(i,c) for c in range(r)]
        cl.append(lits)                       # at least one
        for a in range(r):
            for b in range(a+1, r):
                cl.append([-V(i,a), -V(i,b)]) # at most one
    # forbid monochromatic weak triple x<y, z=x+y
    for x in range(1, N+1):
        for y in range(x+1, N+1):
            z = x+y
            if z > N: break
            for c in range(r):
                cl.append([-V(x,c), -V(y,c), -V(z,c)])
    s = Cadical195(bootstrap_with=cl)
    # symmetry break: integer 1 gets color 0; 2 gets color <=1; small prefix laddered
    s.add_clause([V(1,0)])
    if r>=2: 
        s.add_clause([V(2,0), V(2,1)])
    if seed_assign:
        for i,c in enumerate(seed_assign, start=1):
            if c is not None: s.add_clause([V(i,c)])
    t0=time.time()
    res = s.solve()
    dt=time.time()-t0
    if res:
        model=set(l for l in s.get_model() if l>0)
        coloring=[next(c for c in range(r) if V(i,c) in model) for i in range(1,N+1)]
        return True, coloring, dt
    return False, None, dt

if __name__=='__main__':
    r=int(sys.argv[1]); N=int(sys.argv[2])
    print(f"[ws_sat] solving WS({r}): partition [1,{N}] into {r} weak-sum-free sets ...", flush=True)
    sat, col, dt = solve(N, r)
    if sat:
        ok,d = verify_schur(r, col, weak=True)
        print(f"[ws_sat] SAT in {dt:.1f}s — verifier: {ok} {d}", flush=True)
        if ok:
            json.dump(col, open(f'found_WS{r}_{N}.json','w'))
            print(f"[ws_sat] *** certificate saved: found_WS{r}_{N}.json — proves WS({r}) >= {N} ***", flush=True)
    else:
        print(f"[ws_sat] UNSAT in {dt:.1f}s — WS({r}) < {N} (this N not partitionable)", flush=True)
