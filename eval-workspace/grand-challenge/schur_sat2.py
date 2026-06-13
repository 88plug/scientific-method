"""Strong-Schur SAT with value-symmetry ladder + optional prefix-split for portfolio.
Ladder: color c may be used at integer i only if color c-1 is used at some j<i.
(Standard 'colors appear in order of first use' — kills the 6! permutation symmetry.)"""
import sys, time, json
sys.path.insert(0,'verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def build(N, r):
    vp=IDPool(); V=lambda i,c: vp.id(('x',i,c)); U=lambda i,c: vp.id(('u',i,c)); cl=[]
    for i in range(1,N+1):
        cl.append([V(i,c) for c in range(r)])
        for a in range(r):
            for b in range(a+1,r): cl.append([-V(i,a),-V(i,b)])
    for x in range(1,N+1):
        for y in range(x,N+1):
            z=x+y
            if z>N: break
            for c in range(r): cl.append([-V(x,c),-V(y,c),-V(z,c)])
    # value-symmetry ladder: u[i][c] = color c used at some j<=i
    # V(i,c) -> u[i][c]; u[i][c] -> u[i-1][c] OR V(i,c); and use(c) requires use(c-1) earlier
    cl.append([V(1,0)])
    for c in range(1,r):
        # first integer that may take color c is c+1 (can't introduce color c before c earlier colors seen)
        for i in range(1, c+1): cl.append([-V(i,c)])
    return cl, V, vp

def solve(N, r, prefix=None, tlimit=None):
    cl,V,vp=build(N,r)
    s=Cadical195(bootstrap_with=cl)
    if prefix:
        for i,c in prefix.items(): s.add_clause([V(i,c)])
    t0=time.time(); res=s.solve(); dt=time.time()-t0
    if res:
        m=set(l for l in s.get_model() if l>0)
        col=[next(c for c in range(r) if V(i,c) in m) for i in range(1,N+1)]
        return True,col,dt
    return False,None,dt

if __name__=='__main__':
    r,N=int(sys.argv[1]),int(sys.argv[2])
    print(f"[schur2] S({r}) [1,{N}] with sym-ladder ...", flush=True)
    sat,col,dt=solve(N,r)
    print(f"[schur2] {'SAT' if sat else 'UNSAT'} {dt:.1f}s", flush=True)
    if sat:
        ok,d=verify_schur(r,col,weak=False); print(f"[schur2] verifier {ok} {d}", flush=True)
        if ok: json.dump(col,open(f'found_S{r}_{N}.json','w')); print(f"[schur2] *** saved found_S{r}_{N}.json: S({r})>={N} ***", flush=True)
