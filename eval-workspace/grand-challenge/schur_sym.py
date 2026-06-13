"""Symmetric strong-Schur SAT (Fredricksen-Sweet method): search a sum-free
6-partition of [1,N] symmetric under i <-> (N+1-i). Only ceil(N/2) free colors.
This is the documented record-setting construction restriction."""
import sys, time, json
sys.path.insert(0,'verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def mirror(i,N): return N+1-i

def solve(N, r, exception_pairs=None, tlimit=None):
    vp=IDPool(); cl=[]
    # representative for each symmetry class: rep(i)=min(i, N+1-i). free vars on reps only.
    rep=lambda i: min(i, N+1-i)
    excset=set()
    if exception_pairs:
        for (a,b) in exception_pairs: excset.add(a); excset.add(b)
    def V(i,c):
        # exception integers get their own free var; others share with mirror
        key = i if i in excset else rep(i)
        return vp.id(('x',key,c))
    for i in range(1,N+1):
        cl.append([V(i,c) for c in range(r)])
        for a in range(r):
            for b in range(a+1,r): cl.append([-V(i,a),-V(i,b)])
    for x in range(1,N+1):
        for y in range(x,N+1):
            z=x+y
            if z>N: break
            for c in range(r): cl.append([-V(x,c),-V(y,c),-V(z,c)])
    # symmetry ladder on representatives (value-symmetry break)
    cl.append([V(1,0)])
    s=Cadical195(bootstrap_with=cl)
    t0=time.time(); res=s.solve(); dt=time.time()-t0
    if res:
        m=set(l for l in s.get_model() if l>0)
        col=[next(c for c in range(r) if V(i,c) in m) for i in range(1,N+1)]
        return True,col,dt
    return False,None,dt

if __name__=='__main__':
    N=int(sys.argv[1])
    # 537=3*179 -> 179,358 are the documented exception pair (Fredricksen-Sweet)
    exc=[(179,358)] if N==537 else None
    print(f"[sym] symmetric S(6) [1,{N}] (exception {exc}) ...", flush=True)
    sat,col,dt=solve(N,6,exception_pairs=exc)
    print(f"[sym] {'SAT' if sat else 'UNSAT'} {dt:.1f}s", flush=True)
    if sat:
        ok,d=verify_schur(6,col,weak=False); print(f"[sym] verifier {ok} {d}", flush=True)
        if ok: json.dump(col,open(f'found_S6_{N}_sym.json','w')); print(f"[sym] *** S(6)>={N} saved ***", flush=True)
