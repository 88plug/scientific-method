#!/usr/bin/env python3
"""Parallel multi-restart driver for frontier_sls on S(6)[1,537]. Time-boxed.
Reports per-worker best conflicts; on any verified 0 writes the record cert."""
import sys, time, json, multiprocessing as mp
import frontier_sls as F


def worker(args):
    wid, flips, restarts = args
    trip = F.precompute(F.N)
    pos = F.build_pos_in(trip)
    base = json.load(open("known-certs/schur_6_536.json"))
    seed = [0] * (F.N + 1)
    for i in range(1, 537):
        seed[i] = base[i - 1]
    bestc, bestn = 0, 10 ** 9
    for c in range(F.R):
        n = sum(1 for x in range(1, 269) if base[x - 1] == c and base[537 - x - 1] == c)
        if n < bestn:
            bestc, bestn = c, n
    seed[537] = bestc
    overall = 10 ** 9
    for r in range(restarts):
        rng = F.LCG(2654435761 ^ (wid * 100003 + r * 40503 + 1))
        s = list(seed)
        # perturb the seed a little per restart so workers diverge (keep 1..536 mostly)
        for _ in range(r * 3):
            i = rng.randint(1, 537)
            s[i] = rng.randint(0, F.R - 1)
        col, best, _ = F.run(wid, s, trip, pos, flips, rng)
        if best < overall:
            overall = best
        if best == 0:
            sys.path.insert(0, "verifiers")
            from verify_independent import check_strong_schur
            ok, info = check_strong_schur(F.R, col[1:F.N + 1])
            if ok:
                json.dump(col[1:F.N + 1], open(f"schur6_537_w{wid}.json", "w"))
                return (wid, 0, True, info)
    return (wid, overall, False, "")


def main():
    nworkers = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    flips = int(sys.argv[2]) if len(sys.argv) > 2 else 3_000_000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    t0 = time.time()
    results = []
    with mp.Pool(nworkers) as p:
        for r in p.imap_unordered(worker, [(w, flips, restarts) for w in range(nworkers)]):
            results.append(r)
            print(f"  worker {r[0]} done: best={r[1]} hit={r[2]} ({time.time()-t0:.0f}s)", flush=True)
            if r[2]:
                print(f"*** RECORD by worker {r[0]} — stopping early ***", flush=True)
                break
    dt = time.time() - t0
    best = min(r[1] for r in results)
    hit = [r for r in results if r[2]]
    print(f"=== frontier S(6)[1,537]: {nworkers} workers x {restarts} restarts x {flips} flips, {dt:.0f}s ===")
    print(f"best conflicts across all = {best}")
    if hit:
        print(f"*** RECORD: S(6)>=537 found by worker {hit[0][0]} — {hit[0][3]} ***")
    else:
        print("no 0-conflict coloring found — wall holds (consistent with S(6)=536 exact)")
    print("per-worker bests:", sorted(r[1] for r in results))


if __name__ == "__main__":
    main()
