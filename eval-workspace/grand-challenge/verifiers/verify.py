"""Exact certificate verifiers — pure functions, no envelope, no state.
Each returns (ok: bool, detail: str)."""

def verify_costas(perm):
    """Costas array: permutation of 0..n-1; all displacement vectors distinct."""
    n = len(perm)
    if sorted(perm) != list(range(n)): return False, "not a permutation"
    seen = set()
    for d in range(1, n):
        for i in range(n - d):
            v = (d, perm[i+d] - perm[i])
            if v in seen: return False, f"duplicate vector {v}"
            seen.add(v)
    return True, f"valid Costas array order {n}"

def verify_sorting_network(n, comparators):
    """Zero-one principle: network sorts all 2^n binary inputs."""
    for m in range(2**n):
        v = [(m >> i) & 1 for i in range(n)]
        for (a, b) in comparators:
            if v[a] > v[b]: v[a], v[b] = v[b], v[a]
        if any(v[i] > v[i+1] for i in range(n-1)):
            return False, f"fails on input {m:0{n}b}"
    return True, f"valid sorting network n={n}, size {len(comparators)}"

def verify_capset(n, points):
    """Cap set in F_3^n: no three points (incl. degenerate? no - distinct) sum to 0.
    Equivalent: no line; for distinct a,b,c: a+b+c=0 mod 3 componentwise."""
    pts = [tuple(p) for p in points]
    if len(set(pts)) != len(pts): return False, "duplicate points"
    for p in pts:
        if len(p) != n or any(x not in (0,1,2) for x in p): return False, "bad point"
    S = set(pts)
    m = len(pts)
    for i in range(m):
        for j in range(i+1, m):
            third = tuple((-pts[i][k]-pts[j][k]) % 3 for k in range(n))
            if third in S and third != pts[i] and third != pts[j]:
                return False, f"line found: {pts[i]},{pts[j]},{third}"
    return True, f"valid cap set in F_3^{n}, size {m}"

def verify_vdw(r, k, coloring):
    """vdW lower-bound certificate: coloring of 1..N with r colors, no
    monochromatic k-term arithmetic progression. Proves W(r,k) > N."""
    N = len(coloring)
    if any(c < 0 or c >= r for c in coloring): return False, "bad color"
    for d in range(1, (N - 1) // (k - 1) + 1):
        for a in range(N - (k - 1) * d):
            c0 = coloring[a]
            if all(coloring[a + i*d] == c0 for i in range(1, k)):
                return False, f"mono {k}-AP at start {a+1}, step {d}, color {c0}"
    return True, f"valid: W({r},{k}) > {N}"

def verify_schur(r, coloring, weak=False):
    """Schur certificate: coloring of 1..N, no monochromatic x+y=z
    (weak: x<y<z distinct). Proves S(r)>N (or WS(r)>N)."""
    N = len(coloring)
    col = lambda i: coloring[i-1]
    for x in range(1, N+1):
        for y in range(x if not weak else x+1, N+1):
            z = x + y
            if z > N: break
            if col(x) == col(y) == col(z):
                return False, f"mono triple {x}+{y}={z}"
    return True, f"valid: {'WS' if weak else 'S'}({r}) > {N}"

# ---------- positive controls (verify-the-verifier) ----------
def welch_costas(p, g):
    """Welch construction: order p-1 Costas array from primitive root g mod p."""
    return [pow(g, i+1, p) - 1 for i in range(p-1)]

def batcher_network(n):
    """Batcher odd-even mergesort network (valid, not minimal)."""
    comps=[]
    def merge(lo, cnt, r):
        step = r*2
        if step < cnt:
            merge(lo, cnt, step); merge(lo+r, cnt, step)
            for i in range(lo+r, lo+cnt-r, step): comps.append((i, i+r))
        else:
            comps.append((lo, lo+r))
    def sort(lo, cnt):
        if cnt > 1:
            m = cnt // 2
            sort(lo, m); sort(lo+m, cnt-m)
            mergeall(lo, cnt, 1)
    def mergeall(lo, cnt, r):
        m = r*2
        if m < cnt:
            mergeall(lo, cnt, m); mergeall(lo+r, cnt, m)
            for i in range(lo+r, lo+cnt-r, m):
                if i+r < lo+cnt: comps.append((i, i+r))
        elif lo+r < lo+cnt and lo+r < n:
            comps.append((lo, lo+r))
    # use a simple known-correct generator instead: bitonic for 2^k padded
    comps=[]
    import math
    n2 = 1 << math.ceil(math.log2(n))
    def cmpex(a,b):
        if a<n and b<n: comps.append((a,b))
    def bsort(lo, cnt, direc):
        if cnt>1:
            k=cnt//2
            bsort(lo,k,True); bsort(lo+k,k,False); bmerge(lo,cnt,direc)
    def bmerge(lo,cnt,direc):
        if cnt>1:
            k=cnt//2
            for i in range(lo,lo+k):
                if direc: cmpex(i,i+k)
                else: cmpex(i+k,i)
            bmerge(lo,k,direc); bmerge(lo+k,k,direc)
    bsort(0,n2,True)
    # normalize: ensure (a<b) ordering for ascending net
    return [(min(a,b),max(a,b)) for (a,b) in comps]

if __name__ == '__main__':
    ok,d = verify_costas(welch_costas(11, 2)); print("costas welch p=11:", ok, d)
    bad = welch_costas(11,2); bad[0],bad[1] = bad[1],bad[0]
    print("costas mutated:", verify_costas(bad)[0] == False)
    net = batcher_network(8)
    ok,d = verify_sorting_network(8, net); print("bitonic n=8:", ok, d)
    badnet = net[:-3]
    print("network mutated:", verify_sorting_network(8, badnet)[0] == False)
    # cap set positive control: F_3^2 max cap = 4 (e.g. (0,0),(0,1),(1,0),(1,1)? check)
    cap = [(0,0),(0,1),(1,0),(1,1)]
    ok,d = verify_capset(2, cap); print("capset n=2 size4:", ok, d)
    badcap = [(0,0),(1,1),(2,2)]
    print("capset line rejected:", verify_capset(2, badcap)[0] == False)
    # vdW positive control: W(2,3)=9, so a 2-coloring of 1..8 with no mono 3-AP exists: 0,1,1,0,0,1,1,0? check classic
    ok,d = verify_vdw(2,3,[0,1,1,0,0,1,1,0]); print("vdw 2,3 N=8:", ok, d)
    print("vdw mutated:", verify_vdw(2,3,[0]*8)[0] == False)
    # Schur positive control: S(3)=13 ⇒ 3-coloring of 1..13 exists
    sch = [0,1,1,0,2,2,2,2,0,1,1,0,0]  # known-style; verify
    ok,d = verify_schur(3, sch); print("schur r=3 N=13:", ok, d)
