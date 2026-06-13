"""Strong-Schur SAT: is [1,N] partitionable into r sum-free sets (no x+y=z, x<=y)?
A SAT model proving S(r) >= N. Strong symmetry breaking + restart-friendly CaDiCaL."""
import sys, time, json
sys.path.insert(0,'verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def solve(N, r, seed_assign=None, budget_conf=None):
    vp=IDPool(); V=lambda i,c: vp.id((i,c)); cl=[]
    for i in range(1,N+1):
        cl.append([V(i,c) for c in range(r)])
        for a in range(r):
            for b in range(a+1,r): cl.append([-V(i,a),-V(i,b)])
    nt=0
    for x in range(1,N+1):
        for y in range(x,N+1):          # x<=y  (STRONG)
            z=x+y
            if z>N: break
            for c in range(r): cl.append([-V(x,c),-V(y,c),-V(z,c)]); nt+=1
    s=Cadical195(bootstrap_with=cl)
    # symmetry break: 1->color0; first integer not forced equals a fresh color (value-symmetry ladder)
    s.add_clause([V(1,0)])
    for c in range(1,r):
        # integer (smallest that could be color c) laddered: color c may appear only if c-1 already used below it — approximate ladder
        pass
    if seed_assign:
        for i,c in enumerate(seed_assign, start=1):
            if c is not None: s.add_clause([V(i,c)])
    t0=time.time(); res=s.solve(); dt=time.time()-t0
    if res:
        m=set(l for l in s.get_model() if l>0)
        col=[next(c for c in range(r) if V(i,c) in m) for i in range(1,N+1)]
        return True,col,dt,len(cl)
    return False,None,dt,len(cl)

if __name__=='__main__':
    r=int(sys.argv[1]); N=int(sys.argv[2])
    print(f"[schur] S({r}): strong sum-free {r}-partition of [1,{N}]? ...", flush=True)
    sat,col,dt,nc=solve(N,r)
    print(f"[schur] {'SAT' if sat else 'UNSAT'} {dt:.1f}s ({nc} clauses)", flush=True)
    if sat:
        ok,d=verify_schur(r,col,weak=False)
        print(f"[schur] verifier: {ok} {d}", flush=True)
        if ok:
            json.dump(col,open(f'found_S{r}_{N}.json','w'))
            print(f"[schur] *** saved found_S{r}_{N}.json proves S({r}) >= {N} ***", flush=True)
