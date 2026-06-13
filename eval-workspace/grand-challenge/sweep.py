import sys, time
from wstemplate_sat import solve, check_template

def try_width(a, K, bmax=None, budget=None, verbose=True):
    """Is there ANY b in [1, a-1] giving a valid width-a K-color template?"""
    hi = (a-1) if bmax is None else min(bmax, a-1)
    hits=[]
    for b in range(1, hi+1):
        t0=time.time()
        sat, col, N = solve(a, b, K, budget=budget)
        dt=time.time()-t0
        tag = "SAT" if sat else ("UNSAT" if sat is False else "UNKNOWN")
        if sat:
            ok,msg = check_template(col,a,b,K)
            tag += f"(check={ok})"
            hits.append((a,b,K,col,ok))
        if verbose:
            print(f"  a={a} b={b} K={K} N={N}: {tag} {dt:.1f}s", flush=True)
    return hits

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="teeth":
        # must be UNSAT: K=1 width>=2 (1+2=3 monochrome); also K=2 needs >=2 colors trivially
        for (a,b,K) in [(2,1,1),(4,2,1),(3,1,2)]:
            sat,_,N=solve(a,b,K)
            print(f"teeth (a={a},b={b},K={K}) N={N}: SAT={sat}  (expect: first two UNSAT)")
    else:
        K=int(sys.argv[2]); a0=int(sys.argv[3]); a1=int(sys.argv[4])
        budget=int(sys.argv[5]) if len(sys.argv)>5 else None
        allhits=[]
        for a in range(a0,a1+1):
            allhits += try_width(a,K,budget=budget)
        print("HITS:", [(h[0],h[1],h[2],h[4]) for h in allhits] or "none")
