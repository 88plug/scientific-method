"""Fast incremental strong-Schur SLS. O(degree) per flip via a maintained
violated-triple list (swap-pop) and per-integer violated counts. Seeded from
the 536 cert for the [1,537] attempt. Capability-gated on a small case first."""
import sys, random, time, json
GC = '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge'
sys.path.insert(0, GC + '/verifiers')
from verify import verify_schur

def build(N):
    T = []
    for x in range(1, N + 1):
        for y in range(x, N + 1):
            z = x + y
            if z > N: break
            T.append((x - 1, y - 1, z - 1))   # 0-indexed
    inv = [[] for _ in range(N)]
    for idx, (x, y, z) in enumerate(T):
        inv[x].append(idx); inv[y].append(idx); inv[z].append(idx)
    return T, inv

def run(N, r, seed, init, max_flips, wp=0.4):
    rng = random.Random(seed)
    T, inv = build(N)
    col = list(init)
    mono = bytearray(len(T))
    vlist = []           # indices of currently-mono triples
    pos = [-1] * len(T)  # position in vlist, -1 if absent
    def setmono(idx, on):
        if on and not mono[idx]:
            mono[idx] = 1; pos[idx] = len(vlist); vlist.append(idx)
        elif (not on) and mono[idx]:
            mono[idx] = 0
            p = pos[idx]; last = vlist.pop()
            if p < len(vlist): vlist[p] = last; pos[last] = p
            pos[idx] = -1
    for idx, (x, y, z) in enumerate(T):
        if col[x] == col[y] == col[z]: setmono(idx, True)
    best = len(vlist)
    def recolor(i, c):
        if col[i] == c: return
        for idx in inv[i]:
            if mono[idx]: setmono(idx, False)
        col[i] = c
        for idx in inv[i]:
            x, y, z = T[idx]
            if col[x] == col[y] == col[z]: setmono(idx, True)
    t0 = time.time()
    for flip in range(max_flips):
        if not vlist:
            return col, 0, flip
        idx = vlist[rng.randrange(len(vlist))]
        i = T[idx][rng.randrange(3)]
        if rng.random() < wp:
            recolor(i, rng.randrange(r))
        else:
            cur = col[i]; bestc, bestv = cur, len(vlist)
            for c in range(r):
                if c == cur: continue
                recolor(i, c)
                if len(vlist) < bestv: bestv, bestc = len(vlist), c
                recolor(i, cur)
            recolor(i, bestc)
        if len(vlist) < best:
            best = len(vlist)
        if flip and flip % 2_000_000 == 0 and best > 0:
            for _ in range(max(1, N // 8)):
                recolor(rng.randrange(N), rng.randrange(r))
    return col, best, max_flips

def attempt(N, worker, max_flips):
    base = json.load(open(GC + '/known-certs/schur_6_536.json'))
    rng = random.Random(worker)
    if N == 537:
        init = list(base) + [rng.randrange(6)]
    else:
        init = [rng.randrange(6) for _ in range(N)]
    col, v, flips = run(N, 6, worker, init, max_flips)
    if v == 0 and verify_schur(6, col, weak=False)[0]:
        json.dump(col, open(f'{GC}/RECORD_S6_{N}_sls_w{worker}.json', 'w'))
        return True, flips
    return False, v

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'gate':
        # find S(4)=44 from scratch (known SAT) — must be fast
        t0 = time.time()
        col, v, flips = run(44, 4, 1, [random.Random(1).randrange(4) for _ in range(44)], 2_000_000)
        ok = (v == 0 and verify_schur(4, col, weak=False)[0])
        print(f"[sls gate] S(4)[1,44]: {'SOLVED' if ok else f'best={v}'} {flips} flips {time.time()-t0:.1f}s", flush=True)
    else:
        N = int(sys.argv[2]); worker = int(sys.argv[3]); mf = int(sys.argv[4])
        ok, info = attempt(N, worker, mf)
        print(f"WORKER {worker} N={N}: {'*** SOLVED+VERIFIED RECORD ***' if ok else f'best_viol={info}'}", flush=True)
