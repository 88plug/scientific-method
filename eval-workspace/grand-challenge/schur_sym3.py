"""Symmetric strong-Schur SAT, exception-aware (Fredricksen-Sweet, correct).
sigma(i)=N+1-i, BUT the pair {179,358} is exempt from symmetry-sharing because
358 = (N+1)-179 (mirror) AND 179+179=358 (sum) collide: forcing them equal
contradicts sum-free -> instant UNSAT. F&S place them in different sets. We give
the exempt integers independent colour variables (the documented exception)."""
import sys, time, json
GC = '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge'
sys.path.insert(0, GC + '/verifiers')
from verify import verify_schur
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def find_self_conflicts(N):
    """integers i with N+1-i == 2i (mirror == double) i.e. 3i = N+1 -> i=(N+1)/3."""
    exempt = set()
    if (N + 1) % 3 == 0:
        i = (N + 1) // 3
        exempt.add(i); exempt.add(2 * i)   # i and its mirror/double
    return exempt

def solve(N, r, extra_exempt=None):
    exempt = find_self_conflicts(N)
    if extra_exempt: exempt |= set(extra_exempt)
    vp = IDPool()
    def key(i):
        return ('e', i) if i in exempt else ('x', min(i, N + 1 - i))
    V = lambda i, c: vp.id(key(i) + (c,))
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
                # skip degenerate clauses where two share a var (handled by exemption,
                # but guard anyway): if literals collapse, it's a real unit -> keep only distinct
                lits = {V(x, c), V(y, c), V(z, c)}
                cl.append([-l for l in lits])
    cl.append([V(1, 0)])
    s = Cadical195(bootstrap_with=cl)
    t0 = time.time(); res = s.solve(); dt = time.time() - t0
    if res:
        m = set(l for l in s.get_model() if l > 0)
        col = [next(c for c in range(r) if V(i, c) in m) for i in range(1, N + 1)]
        return True, col, dt, exempt
    return False, None, dt, exempt

if __name__ == '__main__':
    print("[sym3] gate: symmetric exception-aware [1,536] must be SAT ...", flush=True)
    sat, col, dt, ex = solve(536, 6)
    print(f"[sym3] [1,536]: {'SAT' if sat else 'UNSAT'} {dt:.1f}s  exempt={sorted(ex)}", flush=True)
    if sat and verify_schur(6, col, weak=False)[0]:
        print("[sym3] encoder SOUND. Attempting [1,537] ...", flush=True)
        sat2, col2, dt2, ex2 = solve(537, 6)
        print(f"[sym3] [1,537]: {'SAT' if sat2 else 'UNSAT'} {dt2:.1f}s  exempt={sorted(ex2)}", flush=True)
        if sat2 and verify_schur(6, col2, weak=False)[0]:
            json.dump(col2, open(GC + '/RECORD_S6_537_sym3.json', 'w'))
            print("[sym3] *** RECORD CANDIDATE SAVED: S(6) >= 537 *** (verify independently next)", flush=True)
        elif sat2:
            print("[sym3] [1,537] SAT but verifier REJECTED — encoding flaw, discard", flush=True)
        else:
            print("[sym3] symmetric [1,537] UNSAT within budget — frontier holds.", flush=True)
    else:
        print(f"[sym3] gate still failing (sat={sat}) — symmetry model wrong; report frontier on plain track.", flush=True)
