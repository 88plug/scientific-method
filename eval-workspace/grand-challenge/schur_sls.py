"""Strong-Schur stochastic local search (UBCSAT-style), seeded incrementally
from the known [1,536] certificate, extending to [1,537]. The documented
record-setting method for the SAT-find direction near the boundary.
One worker = one seeded multi-start SLS run. Writes a verified cert on success."""
import sys, random, time, json
GC = '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge'
sys.path.insert(0, GC + '/verifiers')
from verify import verify_schur

def triples(N):
    """all (x,y,z) strong: x<=y, x+y=z<=N. Precompute per-z and per-element."""
    T = []
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            z = x + y
            if z > N: break
            T.append((x, y, z))
    return T

def violations(col, T):
    v = 0
    for (x, y, z) in T:
        if col[x-1] == col[y-1] == col[z-1]: v += 1
    return v

def involved(N, T):
    inv = [[] for _ in range(N + 1)]
    for idx, (x, y, z) in enumerate(T):
        inv[x].append(idx); inv[y].append(idx); inv[z].append(idx)
    return inv

def run(N, r, seed, init, max_flips=8_000_000, wp=0.15):
    rng = random.Random(seed)
    T = triples(N); inv = involved(N, T)
    col = list(init)
    # current mono flag per triple
    mono = [col[x-1] == col[y-1] == col[z-1] for (x, y, z) in T]
    viol = sum(mono)
    best = viol
    def recolor(i, c):
        nonlocal viol
        old = col[i-1]
        if old == c: return
        for idx in inv[i]:
            if mono[idx]:
                mono[idx] = False; viol -= 1
        col[i-1] = c
        for idx in inv[i]:
            x, y, z = T[idx]
            if col[x-1] == col[y-1] == col[z-1]:
                if not mono[idx]: mono[idx] = True; viol += 1
    for flip in range(max_flips):
        if viol == 0:
            return col, 0, flip
        # pick a violated triple, pick one of its 3 integers
        vidx = [idx for idx in range(len(T)) if mono[idx]]
        t = T[rng.choice(vidx)]
        i = rng.choice(t)
        if rng.random() < wp:
            recolor(i, rng.randrange(r))
        else:
            # min-conflicts: best color for i
            bestc, bestv = col[i-1], viol
            for c in range(r):
                cur = col[i-1];
                # simulate
                recolor(i, c)
                if viol < bestv: bestv, bestc = viol, c
                recolor(i, cur)
            recolor(i, bestc)
        if viol < best: best = viol
        if flip and flip % 1_000_000 == 0:
            # random restart kick if stuck
            if best > 0:
                for _ in range(N // 10):
                    recolor(rng.randrange(1, N+1), rng.randrange(r))
    return col, best, max_flips

if __name__ == '__main__':
    N = int(sys.argv[1]); worker = int(sys.argv[2])
    base = json.load(open(GC + '/known-certs/schur_6_536.json'))  # 536 colors
    rng = random.Random(worker)
    init = list(base) + [rng.randrange(6)]   # extend to 537 by placing 537 in a random set
    if N != 537: init = init[:N] if N < 537 else init + [rng.randrange(6) for _ in range(N-537)]
    t0 = time.time()
    col, v, flips = run(N, 6, worker, init)
    if v == 0:
        ok, d = verify_schur(6, col, weak=False)
        if ok:
            json.dump(col, open(f'{GC}/RECORD_S6_{N}_sls_w{worker}.json', 'w'))
            print(f"WORKER {worker}: *** SOLVED + VERIFIED S(6)>={N} *** {d} ({flips} flips, {time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"WORKER {worker}: viol=0 but verifier REJECTED ({d}) — bug, discard", flush=True)
    else:
        print(f"worker {worker}: best={v} violations remain ({flips} flips, {time.time()-t0:.0f}s)", flush=True)
