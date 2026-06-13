# Reconstruct the symmetric 6-partition of [1,536] from Fredricksen & Sweet (2000).
# The paper lists "only the smallest of a symmetric pair". n=536, symmetric pair i <-> n+1-i = 537-i.
# 537 = 3*179, so the special-case elements are 179 and 358 = 2*179; paper lists both explicitly.

sets = {
1: [1,5,8,11,14,24,27,30,33,36,40,43,46,49,52,65,71,77,81,84,90,93,99,103,109,112,115,125,128,131,
    134,137,144,147,150,153,160,163,166,169,172,181,185,188,191,194,201,204,207,213,220,223,226,229,232,235,238,242,245,248,251,254,
    264,267,358],
2: [2,12,19,25,26,34,41,57,58,63,72,79,85,86,95,96,102,118,123,124,140,141,145,146,155,156,162,173,183,193,
    200,206,211,215,216,222,233,239,244,253,260,261,266],
3: [3,10,16,22,23,29,35,42,48,56,60,62,67,68,69,74,75,80,87,88,94,100,101,106,107,113,114,119,121,126,
    133,139,151,152,158,159,164,165,171,178,184,192,197,198,203,205,210,217,237,241,243,249,250,255,256],
4: [4,13,20,28,31,38,50,61,64,73,83,91,98,108,110,117,120,132,135,142,143,154,161,168,177,179,187,195,209,212,
    214,219,221,224,231,236,246,258,265],
5: [6,9,17,21,32,39,44,51,54,55,66,70,82,89,92,104,111,127,129,130,149,167,175,189,190,202,225,227,247,252,
    262,263],
6: [7,15,18,37,45,47,53,59,76,78,97,105,116,122,136,138,148,157,170,174,176,180,182,186,196,199,208,218,228,230,
    234,240,257,259,268],
}

N = 536
color = [None]*(N+1)  # 1-indexed
for s, elems in sets.items():
    for i in elems:
        c = s-1  # 0..5
        if color[i] is not None and color[i] != c:
            raise SystemExit(f"conflict listed {i}")
        color[i] = c
        # Special case: 537 = 3*179, so (179, 358) may be in different sets.
        # Both are listed explicitly (179 in set4, 358 in set1); do NOT mirror-link them.
        if i in (179, 358):
            continue
        j = 537 - i
        if 1 <= j <= N:
            if color[j] is not None and color[j] != c:
                raise SystemExit(f"conflict mirror {j} (from {i})")
            color[j] = c

# Check all covered
missing = [i for i in range(1,N+1) if color[i] is None]
if missing:
    raise SystemExit(f"MISSING {len(missing)}: {missing[:20]}")
print("All 536 covered, no listing/mirror conflicts.")

# Verify symmetric property
for i in range(1,N+1):
    j=537-i
    if 1<=j<=N and color[i]!=color[j]:
        if {i,j}=={179,358}:
            continue  # documented exception: 537 divisible by 3
        raise SystemExit(f"not symmetric {i}<->{j}")
print("Symmetric verified (i <-> 537-i; exception pair 179/358 as documented).")

# Verify sum-free: no monochromatic x<=y with x+y=z
bad=0
for c in range(6):
    members=[i for i in range(1,N+1) if color[i]==c]
    mset=set(members)
    for a in members:
        for b in members:
            if a<=b and (a+b) in mset:
                bad+=1
                if bad<=5: print(f"VIOLATION color {c}: {a}+{b}={a+b}")
if bad==0:
    print("SUM-FREE verified: no monochromatic x<=y, x+y=z triple.")
else:
    raise SystemExit(f"{bad} violations")

# Set sizes
from collections import Counter
print("Set sizes (color0..5):", [sum(1 for i in range(1,N+1) if color[i]==c) for c in range(6)])

import json
out=[color[i] for i in range(1,N+1)]  # index n-1 = color of n
with open("/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge/known-certs/schur_6_536.json","w") as f:
    json.dump(out,f)
print("Wrote schur_6_536.json with", len(out), "entries.")
