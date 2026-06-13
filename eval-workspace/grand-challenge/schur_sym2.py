"""Corrected symmetric strong-Schur SAT (Fredricksen-Sweet method, done right).
Search a sum-free r-partition of [1,N] symmetric under sigma(i)=N+1-i.
Representatives: rep(i)=min(i, N+1-i). NO value-symmetry ladder (it conflicts
with the symmetry sharing and killed the known solution), NO hardcoded
exceptions. Only the single safe break: fix integer 1 to colour 0."""
import sys, time, json
GC = '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge'
sys.path.insert(0, GC + '/verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def solve(N, r):
    vp = IDPool()
    rep = lambda i: min(i, N + 1 - i)
    V = lambda i, c: vp.id(('x', rep(i), c))
    cl = []
    for i in range(1, N + 1):
        cl.append([V(i, c) for c in range(r)])
        for a in range(r):
            for b in range(a + 1, r):
                cl.append([-V(i, a), -V(i, b)])
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            z = x + y
            if z > N:
                break
            for c in range(r):
                cl.append([-V(x, c), -V(y, c), -V(z, c)])
    cl.append([V(1, 0)])   # only safe colour-symmetry break
    s = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    res = s.solve()
    dt = time.time() - t0
    if res:
        m = set(l for l in s.get_model() if l > 0)
        col = [next(c for c in range(r) if V(i, c) in m) for i in range(1, N + 1)]
        return True, col, dt
    return False, None, dt

if __name__ == '__main__':
    print("[sym2] correctness gate: symmetric [1,536] must be SAT ...", flush=True)
    sat, col, dt = solve(536, 6)
    print(f"[sym2] symmetric S(6)[1,536]: {'SAT' if sat else 'UNSAT'} {dt:.1f}s", flush=True)
    if sat:
        ok, d = verify_schur(6, col, weak=False)
        print(f"[sym2] verified: {ok} {d}", flush=True)
        if ok:
            print("[sym2] encoder SOUND. Attempting [1,537] (symmetric) ...", flush=True)
            sat2, col2, dt2 = solve(537, 6)
            print(f"[sym2] symmetric S(6)[1,537]: {'SAT' if sat2 else 'UNSAT'} {dt2:.1f}s", flush=True)
            if sat2:
                ok2, d2 = verify_schur(6, col2, weak=False)
                print(f"[sym2] [1,537] verified: {ok2} {d2}", flush=True)
                if ok2:
                    json.dump(col2, open(GC + '/RECORD_S6_537_sym2.json', 'w'))
                    print("[sym2] *** RECORD CANDIDATE SAVED: S(6) >= 537 ***", flush=True)
            else:
                print("[sym2] symmetric [1,537] UNSAT — Fredricksen-Sweet's frontier holds for symmetric search.", flush=True)
    else:
        print("[sym2] STILL BUGGY — symmetry axis wrong; abandon symmetric track.", flush=True)
