"""S(6) record attack, done correctly.
Step 1 (correctness gate): symmetric encoder MUST find the known symmetric
        6-partition of [1,536] (Fredricksen-Sweet). If UNSAT, the encoder is
        buggy -> abort, trust nothing.
Step 2 (the shot): symmetric 6-partition of [1,537]? SAT => NEW RECORD
        (S(6)>=537, and by theorem WS(9)>=22578). CaDiCaL 2023 >> 2000-era tools.
Step 3 (fallback): non-symmetric [1,537] (symmetry can lose solutions).
All results independently re-verified before any claim."""
import sys, time, json
GC = '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge'
sys.path.insert(0, GC + '/verifiers')
sys.path.insert(0, GC)
from verify import verify_schur
import verify_independent as VI
import schur_sym as SYM
import schur_sat2 as PLAIN

def claim_check(N, col, kind):
    a = verify_schur(6, col, weak=False)
    b = VI.check_strong_schur(6, col)
    print(f"    [{kind}] my_verifier={a}  independent={b}", flush=True)
    if a[0] and b[0]:
        f = f"{GC}/RECORD_S6_{N}_{kind}.json"
        json.dump(col, open(f, 'w'))
        print(f"    *** RECORD CERTIFICATE SAVED: {f}  ->  S(6) >= {N} ***", flush=True)
        return True
    print("    !!! verifier disagreement — NOT a valid certificate, discarding", flush=True)
    return False

print("=== STEP 1: correctness gate — symmetric encoder must find known [1,536] ===", flush=True)
t = time.time()
sat, col, dt = SYM.solve(536, 6)
print(f"  symmetric S(6)[1,536]: {'SAT' if sat else 'UNSAT'} in {dt:.1f}s", flush=True)
if not sat:
    print("  ENCODER BUG: a symmetric 6-partition of [1,536] provably exists (Fredricksen-Sweet).", flush=True)
    print("  Aborting symmetric track — would produce false UNSATs. (see fallback)", flush=True)
    encoder_ok = False
else:
    ok, d = verify_schur(6, col, weak=False)
    print(f"  encoder verified: {ok} {d}", flush=True)
    encoder_ok = ok

if encoder_ok:
    print("=== STEP 2: THE SHOT — symmetric 6-partition of [1,537]? ===", flush=True)
    t = time.time()
    sat, col, dt = SYM.solve(537, 6, exception_pairs=[(179, 358)])
    print(f"  symmetric S(6)[1,537]: {'SAT' if sat else 'UNSAT'} in {dt:.1f}s", flush=True)
    if sat:
        print("  >>> SATISFIABLE — candidate new record, verifying independently <<<", flush=True)
        claim_check(537, col, "sym")
    else:
        print("  symmetric [1,537] UNSAT — no symmetric record (matches Fredricksen-Sweet's frontier).", flush=True)

print("=== STEP 3: fallback — non-symmetric [1,537] (symmetry can lose solutions) ===", flush=True)
t = time.time()
sat, col, dt = PLAIN.solve(537, 6)
print(f"  plain S(6)[1,537]: {'SAT' if sat else 'UNSAT'} in {dt:.1f}s", flush=True)
if sat:
    print("  >>> SATISFIABLE — candidate new record, verifying independently <<<", flush=True)
    claim_check(537, col, "plain")
else:
    print("  plain [1,537] UNSAT within budget.", flush=True)

print("=== ATTACK COMPLETE ===", flush=True)
