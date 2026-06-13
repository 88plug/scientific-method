#!/usr/bin/env python3
"""
THIRD independent check of the WS-template UNSAT claims, sharing NO code with the
pysat one-hot encoder (build()) -- a direct backtracking search over Def 3.13.
Constraints re-derived here from scratch; only `pi` is imported (pure arithmetic).
If this finds no template for a width, that width is independently confirmed empty.
"""
import sys
from wstemplate_sat import pi   # pure arithmetic map only


def exists_template(a, b, K):
    """DFS color elements 1..N; prune on first violation. Returns a witness or None."""
    N = a + b
    f = [0] * (N + 1)          # f[x] in 1..K, 0 = unassigned

    def ok(x, c):
        # place color c at x; check all constraints involving x and already-colored elements
        # P1 weak (y<x, y+x in D): f[y]=c and f[x+y]=c forbidden; also pairs summing to x
        for y in range(1, x):
            if f[y] != c:
                continue
            s = x + y
            if s <= N and f[s] == c:
                return False
        # pairs (y,z) y+z=x already colored c with z!=y -> f[x] must != c (weak), checked when both<x:
        for y in range(1, x):
            z = x - y
            if 1 <= z < x and y != z and f[y] == c and f[z] == c and c == c:
                # x is the sum of two distinct same-color elements -> weak forbids f[x]=c
                return False
        # P2 sum-free doubling for elements > b: y>b, 2y=x  -> f[y]=c forbids f[x]=c
        if x % 2 == 0:
            y = x // 2
            if y > b and f[y] == c:
                return False
        for y in range(1, x):           # x doubled lands beyond x; check when 2x<=N handled at 2x
            pass
        # special pin
        if x == a and c != K:
            return False
        if x == a:
            pass
        # closure P3 (non-special c<K): pairs (y,z) y+z=s>N, pi(s)=x, f[y]=f[z]=c -> f[x]!=c
        if c < K:
            for y in range(1, x + 1):
                for z in range(y, N + 1):
                    s = y + z
                    if s <= N:
                        continue
                    if pi(s, a, b) != x:
                        continue
                    if y < x and z < x and f[y] == c and f[z] == c:
                        return False
        # closure P4 (special c==K): pairs (y,z) y+z=s>2a+b, s-2a=x, f[y]=f[z]=K -> f[x]!=K
        if c == K:
            for y in range(1, x):
                for z in range(y, N + 1):
                    s = y + z
                    if s <= 2 * a + b:
                        continue
                    if s - 2 * a != x:
                        continue
                    if z < x and f[y] == K and f[z] == K:
                        return False
        return True

    # also need: when we color x, the doubling 2x and sums with later elements get checked later.
    def dfs(x):
        if x > N:
            return dict(enumerate(f))   # full assignment
        for c in range(1, K + 1):
            if x == a and c != K:
                continue
            if ok(x, c):
                f[x] = c
                if dfs(x + 1) is not None:
                    return {i: f[i] for i in range(1, N + 1)}
                f[x] = 0
        return None

    return dfs(1)


if __name__ == "__main__":
    cases = [(int(sys.argv[i]), int(sys.argv[i + 1]), int(sys.argv[i + 2]))
             for i in range(1, len(sys.argv), 3)] or \
            [(4, 2, 2), (13, 8, 3),           # witnesses: MUST find
             (5, 2, 2), (6, 2, 2),            # K=2 ceiling: must be empty
             (14, 2, 3), (14, 7, 3), (20, 10, 3)]   # K=3 ceiling samples: must be empty
    from wstemplate_sat import check_template
    for (a, b, K) in cases:
        w = exists_template(a, b, K)
        if w:
            valid = check_template(w, a, b, K)[0]
            print(f"(a={a},b={b},K={K}): TEMPLATE FOUND, independent-valid={valid}")
        else:
            print(f"(a={a},b={b},K={K}): no template (independent DFS, empty)")
