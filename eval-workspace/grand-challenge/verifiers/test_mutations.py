"""Verify-the-verifier: each published cert must ACCEPT, and 3 mutations of each
must be REJECTED by the independent checkers in verify_independent.py."""

import copy
import json
import os

from verify_independent import (
    check_weak_schur, check_strong_schur, check_capset, check_vdw)

CERTS = os.path.join(os.path.dirname(__file__), "..", "known-certs")


def load(name):
    with open(os.path.join(CERTS, name)) as fh:
        return json.load(fh)


def expect_accept(label, ok):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] accept {label}")
    return ok


def expect_reject(label, res):
    ok = not res[0]
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] reject {label}: {res[1]}")
    return ok


all_pass = True


# ---- weak Schur (use wschur_5_196, r=5) ----------------------------------
print("weak Schur WS(5)>=196 :")
col = load("wschur_5_196.json")
all_pass &= expect_accept("original", check_weak_schur(5, col)[0])

# mutation 1: flip one cell to manufacture a mono triple. Integers 1,2,3 are
# colored [1,1,2]; force index 2 (integer 3) to color 1 -> 1+2=3 all color 1.
m1 = copy.deepcopy(col); m1[2] = 1
all_pass &= expect_reject("mut1 force 1+2=3 mono", check_weak_schur(5, m1))

# mutation 2: collapse all of color 5's region into color 1 (introduces triples).
m2 = [1 if c == 5 else c for c in col]
all_pass &= expect_reject("mut2 merge color 5 into 1", check_weak_schur(5, m2))

# mutation 3: exceed the color budget (introduce a 6th color).
m3 = copy.deepcopy(col); m3[0] = 6
all_pass &= expect_reject("mut3 color budget r=5 exceeded", check_weak_schur(5, m3))


# ---- strong Schur: confirm the original is NOT a strong cert, and that a
#      genuinely strong-valid small coloring is accepted + mutated. ----------
print("strong Schur sanity :")
# Known: S(3) >= 13 via the standard coloring of 1..13 with 3 colors.
# Build a valid strong-Schur 3-coloring of 1..13 (a known sum-free partition).
s13 = [1,2,2,1,3,3,1,3,3,1,2,2,1]  # brute-forced valid strong-Schur 3-coloring of 1..13
all_pass &= expect_accept("S(3)>=13 witness", check_strong_schur(3, s13)[0])
ms1 = copy.deepcopy(s13); ms1[1] = 3   # break it
all_pass &= expect_reject("mut1 perturb cell", check_strong_schur(3, ms1))
ms2 = [1]*13                            # all one color -> 1+1=2 mono
all_pass &= expect_reject("mut2 monochrome", check_strong_schur(3, ms2))
ms3 = copy.deepcopy(s13); ms3[0] = 9   # 9 colors > r=3
all_pass &= expect_reject("mut3 color budget", check_strong_schur(3, ms3))


# ---- cap set n=8, size 512 ------------------------------------------------
print("cap set F_3^8 size 512 :")
pts = load("capset_n8_512.json")
all_pass &= expect_accept("original", check_capset(8, pts)[0])

# mutation 1: duplicate a point.
c1 = copy.deepcopy(pts); c1.append(list(pts[0]))
all_pass &= expect_reject("mut1 duplicate point", check_capset(8, c1))

# mutation 2: replace a point with one completing a line of two existing pts.
# Take pts[0],pts[1]; the completing point c=-(a+b) mod3 forms a line.
a, b = pts[0], pts[1]
c = [(-(ai + bi)) % 3 for ai, bi in zip(a, b)]
c2 = copy.deepcopy(pts); c2[2] = c   # overwrite some other point with c
all_pass &= expect_reject("mut2 inject collinear point", check_capset(8, c2))

# mutation 3: corrupt a coordinate out of F_3.
c3 = copy.deepcopy(pts); c3[0] = [3] + list(pts[0][1:])
all_pass &= expect_reject("mut3 coord not in F_3", check_capset(8, c3))


# ---- van der Waerden (use vdw_7_3_343, r=7,k=3) ---------------------------
print("vdW W(7,3)>343 :")
col = load("vdw_7_3_343.json")
all_pass &= expect_accept("original", check_vdw(7, 3, col)[0])

# mutation 1: force a mono 3-AP at positions 1,2,3 (a=1,d=1).
v1 = copy.deepcopy(col); v1[0] = v1[1] = v1[2] = 0
all_pass &= expect_reject("mut1 force 1,2,3 AP", check_vdw(7, 3, v1))

# mutation 2: collapse to a single color (massive AP).
v2 = [0]*len(col)
all_pass &= expect_reject("mut2 monochrome", check_vdw(7, 3, v2))

# mutation 3: exceed color budget r=7 (introduce color 7).
v3 = copy.deepcopy(col); v3[0] = 7
all_pass &= expect_reject("mut3 color budget", check_vdw(7, 3, v3))


print()
print("ALL TESTS PASS" if all_pass else "*** SOME TESTS FAILED ***")
