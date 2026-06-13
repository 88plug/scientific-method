"""Independent certificate checkers, written from mathematical definitions only.

This is a SECOND, from-scratch verifier (the witness-artifact rule): it does NOT
read or import the builder's verify.py. Each checker takes the explicit problem
parameters plus the witness object and returns (is_valid, reason).

Coloring lists are 0-indexed Python lists representing the colors of the integers
1..N in order (coloring[i] is the color of integer i+1). Colors may be any hashable
labels; we never assume a particular color alphabet.
"""

from itertools import combinations


# ---------------------------------------------------------------------------
# 1. Weak Schur: WS(r) >= N
#     No monochromatic solution of x + y = z with 1 <= x < y, z = x+y <= N.
#     (Distinct x,y; the "weak" condition forbids x = y.)
# ---------------------------------------------------------------------------
def check_weak_schur(r, coloring):
    N = len(coloring)
    if r is not None and len(set(coloring)) > r:
        return False, f"uses {len(set(coloring))} colors but r={r}"
    # color_of(integer v) = coloring[v-1]
    for x in range(1, N + 1):
        cx = coloring[x - 1]
        for y in range(x + 1, N + 1):       # strict x < y
            z = x + y
            if z > N:
                break
            if cx == coloring[y - 1] == coloring[z - 1]:
                return False, f"mono weak-Schur triple x={x} y={y} z={z} color={cx}"
    return True, f"valid weak-Schur coloring, WS({r}) >= {N}"


# ---------------------------------------------------------------------------
# 2. Strong Schur: S(r) >= N
#     No monochromatic solution of x + y = z with 1 <= x <= y, z <= N.
#     (Allows x = y, i.e. 2x = z.)
# ---------------------------------------------------------------------------
def check_strong_schur(r, coloring):
    N = len(coloring)
    if r is not None and len(set(coloring)) > r:
        return False, f"uses {len(set(coloring))} colors but r={r}"
    for x in range(1, N + 1):
        cx = coloring[x - 1]
        for y in range(x, N + 1):           # x <= y, allows x == y
            z = x + y
            if z > N:
                break
            if cx == coloring[y - 1] == coloring[z - 1]:
                return False, f"mono strong-Schur triple x={x} y={y} z={z} color={cx}"
    return True, f"valid strong-Schur coloring, S({r}) >= {N}"


# ---------------------------------------------------------------------------
# 3. Cap set in F_3^n
#     No three DISTINCT collinear points. Three points a,b,c are collinear in
#     F_3 iff a + b + c == 0 (mod 3) componentwise. For distinct points this is
#     equivalent to "no 3-term line", since in F_3 a line through two distinct
#     points a,b has third point c = -(a+b) = 2a+2b (mod 3).
# ---------------------------------------------------------------------------
def check_capset(n, points):
    # structural checks
    pts = [tuple(p) for p in points]
    for p in pts:
        if len(p) != n:
            return False, f"point {p} has dimension {len(p)} != n={n}"
        if any(c not in (0, 1, 2) for c in p):
            return False, f"point {p} has a coordinate not in F_3"
    if len(set(pts)) != len(pts):
        return False, "duplicate points in the cap set"
    pset = set(pts)
    # For each unordered pair {a,b}, the unique completing point c making a line
    # is c = (-(a_i + b_i)) mod 3 per coordinate. If c is in the set and c is
    # distinct from a and b, we have three distinct collinear points.
    for a, b in combinations(pts, 2):
        c = tuple((-(ai + bi)) % 3 for ai, bi in zip(a, b))
        if c in pset and c != a and c != b:
            return False, f"collinear distinct triple {a},{b},{c}"
    return True, f"valid cap set of size {len(pts)} in F_3^{n}"


# ---------------------------------------------------------------------------
# 4. van der Waerden: W(r,k) > N
#     No monochromatic k-term arithmetic progression in the coloring of 1..N.
#     A k-AP is {a, a+d, ..., a+(k-1)d} with d >= 1, all terms in [1,N].
# ---------------------------------------------------------------------------
def check_vdw(r, k, coloring):
    N = len(coloring)
    if r is not None and len(set(coloring)) > r:
        return False, f"uses {len(set(coloring))} colors but r={r}"
    if k < 1:
        return False, f"k={k} invalid"
    for a in range(1, N + 1):
        ca = coloring[a - 1]
        max_d = (N - a) // (k - 1) if k > 1 else 0
        for d in range(1, max_d + 1):
            # check whole AP is monochromatic
            for j in range(1, k):
                if coloring[a + j * d - 1] != ca:
                    break
            else:
                terms = [a + j * d for j in range(k)]
                return False, f"mono {k}-AP {terms} color={ca}"
    return True, f"valid coloring with no mono {k}-AP, W({r},{k}) > {N}"


# ---------------------------------------------------------------------------
# CLI / self-test harness
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    import os
    import sys

    certs_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "known-certs")

    def load(name):
        with open(os.path.join(certs_dir, name)) as fh:
            return json.load(fh)

    print("=== Validating published record certificates ===")

    # weak Schur certs
    for fn, r, N in [("wschur_5_196.json", 5, 196), ("wschur_6_572.json", 6, 572)]:
        col = load(fn)
        wv, wr = check_weak_schur(r, col)
        sv, sr = check_strong_schur(r, col)
        print(f"{fn}: weak={wv} ({wr}) | strong={sv} ({sr})")

    # cap set
    col = load("capset_n8_512.json")
    v, msg = check_capset(8, col)
    print(f"capset_n8_512.json: {v} ({msg})")

    # vdW certs (filename vdw_<r>_<k>_<N>)
    for fn in sorted(f for f in os.listdir(certs_dir) if f.startswith("vdw_")):
        parts = fn[:-5].split("_")
        r, k, N = int(parts[1]), int(parts[2]), int(parts[3])
        col = load(fn)
        v, msg = check_vdw(r, k, col)
        print(f"{fn}: {v} ({msg})")
