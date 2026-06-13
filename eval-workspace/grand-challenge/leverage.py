#!/usr/bin/env python3
"""Time-boxed leverage search for record-beating WS-templates (K>=5).
Gate sanity: K=5 should re-find the known a=127 template (SAT) before any
larger-width claim is trusted. A SAT hit is written to a json cert and must
later be composed via Theorem 3.17 and checked by verify_schur(weak=True)."""
import sys, time, json
from wstemplate_sat import solve, check_template

K = int(sys.argv[1]); a0 = int(sys.argv[2]); a1 = int(sys.argv[3])
budget = int(sys.argv[4]) if len(sys.argv) > 4 else 200000   # conflicts/instance

for a in range(a0, a1 + 1):
    lo = int(0.40 * a); hi = int(0.62 * a)
    for b in range(max(1, lo), min(a - 1, hi) + 1):
        t = time.time(); sat, col, N = solve(a, b, K, budget=budget); dt = time.time() - t
        if sat:
            ok, msg = check_template(col, a, b, K)
            print(f"*** a={a} b={b} K={K} N={N}: SAT check={ok} {dt:.1f}s ***", flush=True)
            if ok:
                json.dump({"a": a, "b": b, "K": K, "coloring": {str(k): v for k, v in col.items()}},
                          open(f"wstemplate_a{a}_b{b}_K{K}.json", "w"))
        elif sat is False:
            print(f"a={a} b={b} K={K} N={N}: UNSAT {dt:.1f}s", flush=True)
        else:
            print(f"a={a} b={b} K={K} N={N}: UNKNOWN(budget) {dt:.1f}s", flush=True)
print("LEVERAGE_DONE", flush=True)
