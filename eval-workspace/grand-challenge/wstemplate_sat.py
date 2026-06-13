#!/usr/bin/env python3
"""
b-WS-template SAT encoder  (Ageron, Coulon-Lauture, Le Gall  arXiv:2112.03175, Def 3.13)
and the Theorem-3.17 verifier that turns any found template into a checkable WS bound.

A b-WS-template with width a and K colors is a partition of [[1, a+b]] into colors
1..K (special color = K, and the integer `a` must be colored K) satisfying, with
the closure map pi_{a,b}:

    r = s mod a ; pi(s) = r + a  if r in {0..b} else r        (codomain [[b+1, a+b]])

  P1  weakly sum-free (every color, x != y):
        x,y in D, x<y, s=x+y in D, f(x)=f(y)=c  =>  f(s) != c
  P2  sum-free for elements > b (the x=y case; x<y already in P1):
        x in [[b+1,a+b]], s=2x in D, f(x)=c  =>  f(2x) != c
  P3  closure, NON-special colors c in 1..K-1 (Def 3.13 C4):
        x,y in D, s=x+y > a+b, t=pi(s), f(x)=f(y)=c  =>  f(t) != c
  P4  closure, SPECIAL color K (Def 3.13 C3):
        x,y in D, s=x+y > 2a+b, t=s-2a, f(x)=f(y)=K  =>  f(t) != K

Why this is honest: a valid template composes (Thm 3.17) with a sum-free k-partition
of [[1,p]] into a WEAK partition of [[1, p*a + b]] -- which my already-validated
verify_schur(weak=True) checks directly. So nothing here is trusted on its own
encoding; a "record" is only claimed after the composed weak partition is accepted
by the independent checker.
"""
import sys, time
from pysat.formula import CNF
from pysat.solvers import Cadical195


def pi(s, a, b):
    r = s % a
    return r + a if 0 <= r <= b else r


def build(a, b, K, fixed=None, symbreak=False):
    """Return (cnf, var) for a width-a, K-color b-WS-template on [[1,a+b]].
    `fixed`: optional dict {x: color} to pin (used by the gate to test a known template).
    `symbreak`: order the NON-special colors 1..K-1 by first appearance (Crawford
    precede). Lossless -- any template can be relabeled so its non-special colors are
    introduced in index order -- so a SAT hit under symbreak is a genuine template and
    UNSAT under symbreak is UNSAT overall. Special color K is left free (pinned by a)."""
    N = a + b
    D = range(1, N + 1)
    # var(x,c) = literal id ; one-hot coloring
    idx = {}
    nv = 0
    for x in D:
        for c in range(1, K + 1):
            nv += 1
            idx[(x, c)] = nv
    var = lambda x, c: idx[(x, c)]
    cnf = CNF()

    # exactly-one color per element
    for x in D:
        cnf.append([var(x, c) for c in range(1, K + 1)])           # at least one
        for c1 in range(1, K + 1):
            for c2 in range(c1 + 1, K + 1):
                cnf.append([-var(x, c1), -var(x, c2)])              # at most one

    # `a` is special (color K)
    cnf.append([var(a, K)])

    # optional pins (gate / symmetry-seed)
    if fixed:
        for x, c in fixed.items():
            cnf.append([var(x, c)])

    # symmetry break: non-special colors introduced in index order (Crawford precede)
    if symbreak:
        cnf.append([var(1, 1)])                                # elem 1 takes first color
        for x in D:
            for c in range(2, K):                              # non-special 2..K-1
                # var(x,c) -> some y<x has color c-1
                cnf.append([-var(x, c)] + [var(y, c - 1) for y in range(1, x)])

    # P1 weakly sum-free  (all colors, x<y, s in D)
    for x in D:
        for y in range(x + 1, N + 1):
            s = x + y
            if s > N:
                break
            for c in range(1, K + 1):
                cnf.append([-var(x, c), -var(y, c), -var(s, c)])

    # P2 sum-free, x=y case for elements > b
    for x in range(b + 1, N + 1):
        s = 2 * x
        if s > N:
            break
        for c in range(1, K + 1):
            cnf.append([-var(x, c), -var(s, c)])

    # P3 closure for NON-special colors (s > a+b -> pi)
    for x in D:
        for y in range(x, N + 1):           # include x==y
            s = x + y
            if s <= N:
                continue
            t = pi(s, a, b)
            for c in range(1, K):           # 1..K-1
                if x == y:
                    cnf.append([-var(x, c), -var(t, c)])
                else:
                    cnf.append([-var(x, c), -var(y, c), -var(t, c)])

    # P4 closure for SPECIAL color K (s > 2a+b -> s-2a)
    for x in D:
        for y in range(x, N + 1):           # include x==y
            s = x + y
            if s <= 2 * a + b:
                continue
            t = s - 2 * a
            if not (1 <= t <= N):
                continue
            if x == y:
                cnf.append([-var(x, K), -var(t, K)])
            else:
                cnf.append([-var(x, K), -var(y, K), -var(t, K)])

    return cnf, var, N


def solve(a, b, K, fixed=None, budget=None, symbreak=False):
    cnf, var, N = build(a, b, K, fixed, symbreak)
    s = Cadical195(bootstrap_with=cnf.clauses)
    if budget:
        s.conf_budget(budget)
        sat = s.solve_limited(expect_interrupt=True)
    else:
        sat = s.solve()
    coloring = None
    if sat:
        model = set(l for l in s.get_model() if l > 0)
        coloring = {}
        for x in range(1, N + 1):
            for c in range(1, K + 1):
                if var(x, c) in model:
                    coloring[x] = c
    s.delete()
    return sat, coloring, N


# ---- independent pure-python checker of Def 3.13 (does NOT reuse the encoder) ----
def check_template(coloring, a, b, K):
    N = a + b
    assert set(coloring) == set(range(1, N + 1)), "not a full coloring of [[1,a+b]]"
    assert all(1 <= c <= K for c in coloring.values()), "color out of range"
    f = coloring
    if f[a] != K:
        return False, f"a={a} not in special color K={K} (got {f[a]})"
    # P1 weak
    for x in range(1, N + 1):
        for y in range(x + 1, N + 1):
            s = x + y
            if s > N:
                break
            if f[x] == f[y] == f[s]:
                return False, f"weak sum-free violated: {x}+{y}={s} all color {f[x]}"
    # P2 sum-free x=y, elem>b
    for x in range(b + 1, N + 1):
        s = 2 * x
        if s > N:
            break
        if f[x] == f[s]:
            return False, f"sum-free(2x) violated: {x}+{x}={s} color {f[x]}"
    # P3 closure non-special
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            s = x + y
            if s <= N:
                continue
            t = pi(s, a, b)
            c = f[x]
            if c <= K - 1 and f[y] == c and f[t] == c:
                return False, f"P3 closure violated: {x}+{y}={s}->pi={t} color {c}"
    # P4 closure special
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            s = x + y
            if s <= 2 * a + b:
                continue
            t = s - 2 * a
            if not (1 <= t <= N):
                continue
            if f[x] == K and f[y] == K and f[t] == K:
                return False, f"P4 closure violated: {x}+{y}={s}->{t} special"
    return True, "valid b-WS-template"


KNOWN = {
    # (a,b,K): {x: color}  -- special color = K
    (4, 2, 2): {1: 1, 2: 1, 6: 1, 3: 2, 4: 2, 5: 2},                      # Rowley order-6, special A2={3,4,5}
    (13, 8, 3): {**{x: 1 for x in (1, 2, 4, 8, 21)},
                 **{x: 2 for x in (3, 5, 6, 7, 18, 19, 20)},
                 **{x: 3 for x in range(9, 18)}},                          # Rowley [1,21], special A3={9..17}
}


def gate():
    ok = True
    for (a, b, K), col in KNOWN.items():
        valid, msg = check_template(col, a, b, K)
        sat, found, N = solve(a, b, K)
        line = f"GATE (a={a},b={b},K={K}) N={N}: known-valid={valid} ({msg}); solver SAT={sat}"
        print(line)
        if not valid or not sat:
            ok = False
    print("GATE", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "gate":
        sys.exit(0 if gate() else 1)
    # search:  wstemplate_sat.py search a b K [conf_budget]
    _, _, a, b, K = sys.argv[:5]
    a, b, K = int(a), int(b), int(K)
    budget = int(sys.argv[5]) if len(sys.argv) > 5 else None
    t0 = time.time()
    sat, col, N = solve(a, b, K, budget=budget)
    dt = time.time() - t0
    print(f"(a={a},b={b},K={K}) N={N}  SAT={sat}  {dt:.2f}s")
    if sat:
        valid, msg = check_template(col, a, b, K)
        print("  self-check:", valid, msg)
        print("  coloring:", {c: sorted(x for x in col if col[x] == c) for c in range(1, K + 1)})
