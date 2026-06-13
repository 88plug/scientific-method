#!/usr/bin/env python3
"""
Record-grade frontier SLS for strong Schur S(6): seed from the Fredricksen-Sweet
[1,536] partition, try to reach a conflict-free 6-coloring of [1,537] (=> S(6)>=537,
a new record). This is the reopening condition the campaign's falsification log left:
NOT naive uniform min-conflicts (already killed) but a frontier-weighted objective
seeded from the record, with multi-restart.

Any 0-conflict result is gated by verify_independent.check_strong_schur before any
claim. If it plateaus, that is the record-grade method also hitting the wall -> the
honest measured frontier (and S(6)=536 almost surely exact).

No Date/random from the harness; we use a local PRNG seeded by an integer arg so runs
are reproducible and varied by worker id.
"""
import json, sys, time

N = 537
R = 6


def precompute(N):
    # for each z, list of (x,y) x<=y, x+y=z  -> the Schur triples ending at z
    trip = [[] for _ in range(N + 1)]
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            z = x + y
            if z > N:
                break
            trip[z].append((x, y))
    return trip


class LCG:
    def __init__(self, s): self.s = s & 0xFFFFFFFF
    def nxt(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s
    def rand(self): return self.nxt() / 0x7FFFFFFF
    def randint(self, a, b): return a + self.nxt() % (b - a + 1)


def conflicts_at(col, z, trip):
    c = col[z]
    n = 0
    for (x, y) in trip[z]:
        if col[x] == c and col[y] == c:
            n += 1
    return n


def total_conflicts(col, trip):
    t = 0
    for z in range(1, N + 1):
        t += conflicts_at(col, z, trip)
    return t


def delta_if(col, i, newc, trip, pos_in):
    """change in total conflicts if element i recolored to newc.
    pos_in[i] = list of z where i participates as x or y (z=i+other), plus z=i itself."""
    old = col[i]
    if old == newc:
        return 0
    d = 0
    # triples where i is the summed value z=i
    for (x, y) in trip[i]:
        a, b = col[x], col[y]
        if a == b:
            if a == old:
                d -= 1
            if a == newc:
                d += 1
    # triples where i is one of the addends (z = i + other)
    for z, other in pos_in[i]:
        cz = col[z]
        if other == i:
            # doubling triple (i,i,2i): BOTH addends are i and change together
            co_old = old
            co_new = newc
        else:
            co_old = col[other]
            co_new = col[other]
        if old == co_old == cz:
            d -= 1
        if newc == co_new == cz:
            d += 1
    return d


def build_pos_in(trip):
    pos_in = [[] for _ in range(N + 1)]
    for z in range(1, N + 1):
        for (x, y) in trip[z]:
            pos_in[x].append((z, y))
            if y != x:
                pos_in[y].append((z, x))
    return pos_in


def run(worker, seed_col, trip, pos_in, max_flips, rng):
    col = list(seed_col)
    cur = total_conflicts(col, trip)
    best = cur
    for flip in range(max_flips):
        if flip % 50000 == 0:
            cur = total_conflicts(col, trip)        # resync against drift
        if cur == 0:
            return col, 0, flip
        # find a conflicted z (frontier-weighted: prefer larger z)
        confz = [z for z in range(N, 0, -1) if conflicts_at(col, z, trip) > 0]
        if not confz:
            return col, 0, flip
        # pick a conflict near the frontier with bias, else random
        z = confz[0] if rng.rand() < 0.5 else confz[rng.randint(0, len(confz) - 1)]
        # candidate elements to recolor: the triple members at z
        cands = set()
        for (x, y) in trip[z]:
            if col[x] == col[y] == col[z]:
                cands.update((x, y, z))
        if not cands:
            continue
        cands = list(cands)
        # min-conflicts move with walk noise
        if rng.rand() < 0.25:
            i = cands[rng.randint(0, len(cands) - 1)]
            nc = rng.randint(0, R - 1)
            d = delta_if(col, i, nc, trip, pos_in)
            col[i] = nc; cur += d
        else:
            bi, bnc, bd = None, None, 10 ** 9
            for i in cands:
                for nc in range(R):
                    if nc == col[i]:
                        continue
                    d = delta_if(col, i, nc, trip, pos_in)
                    if d < bd or (d == bd and rng.rand() < 0.3):
                        bi, bnc, bd = i, nc, d
            if bi is not None:
                col[bi] = bnc; cur += bd
        if cur < best:
            best = cur
    return col, best, max_flips


def main():
    worker = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    max_flips = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
    trip = precompute(N)
    pos_in = build_pos_in(trip)
    base = json.load(open("known-certs/schur_6_536.json"))   # 536 colors, 0..5
    # seed: 1..536 from record (col index 0..535), 537 placed in best color
    seed = [0] * (N + 1)
    for i in range(1, 537):
        seed[i] = base[i - 1]
    # best color for 537
    bestc, bestn = 0, 10 ** 9
    for c in range(R):
        n = sum(1 for x in range(1, 269) if base[x - 1] == c and base[537 - x - 1] == c)
        if n < bestn:
            bestc, bestn = c, n
    seed[537] = bestc
    rng = LCG(2654435761 ^ (worker * 40503 + 1))
    t0 = time.time()
    col, best, flips = run(worker, seed, trip, pos_in, max_flips, rng)
    dt = time.time() - t0
    print(f"worker {worker}: best_conflicts={best} flips={flips} {dt:.0f}s", flush=True)
    if best == 0:
        sys.path.insert(0, "verifiers")
        from verify_independent import check_strong_schur
        ok, info = check_strong_schur(R, col[1:N + 1])
        print(f"  *** 0 CONFLICTS — verify_independent: {ok} {info} ***", flush=True)
        if ok:
            json.dump(col[1:N + 1], open(f"schur6_537_w{worker}.json", "w"))
            print("  *** RECORD CANDIDATE WRITTEN ***", flush=True)


if __name__ == "__main__":
    main()
