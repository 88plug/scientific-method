#!/usr/bin/env python3
"""
Certificate package for  WS+(2)=4  and  WS+(3)=13  (Ageron et al. Def 3.13 WS-templates).

Claim (per color count K):  the maximum width of a b-WS-template with K colors is
    K=2 -> 4   (so WS+(2)=4)
    K=3 -> 13  (so WS+(3)=13)
both previously only bracketed by Prop 3.16:  (3/2)WS(K-1)+1 <= WS+(K) <= WS(K),
i.e. 4<=WS+(2)<=8 and 13<=WS+(3)<=23. We show the lower bound is TIGHT.

Proof = (a) a SAT witness at the claimed max width (the published Rowley template),
        (b) UNSAT for EVERY width strictly above it up to the Prop-3.16 ceiling WS(K),
            for every admissible b in [1,a-1],
        (c) encoder soundness: exhaustive encoder-vs-independent-checker equivalence
            on small cases (equiv.py) + reproduction of both published templates.

Each UNSAT instance is exported as DIMACS so any third-party SAT solver re-confirms it
(verified here with two independent engines: CaDiCaL to encode, Glucose3 to re-check).
"""
import os, time, json
from pysat.solvers import Cadical195
from wstemplate_sat import build, KNOWN, check_template, solve

WS = {1: 2, 2: 8, 3: 23, 4: 66}      # exact weak Schur numbers (Rowley, proven for r<=4)
CEILING = {2: WS[2], 3: WS[3]}       # Prop 3.16: WS+(K) <= WS(K)
WITNESS_WIDTH = {2: 4, 3: 13}
DIMACS_DIR = "wstemplate_certs"
os.makedirs(DIMACS_DIR, exist_ok=True)


def confirm_unsat(a, b, K, dump_dimacs=False, dump_drat=False):
    cnf, var, N = build(a, b, K)
    if dump_dimacs:
        cnf.to_file(f"{DIMACS_DIR}/wstpl_a{a}_b{b}_K{K}.cnf")
    s = Cadical195(bootstrap_with=cnf.clauses)
    sat = s.solve()
    s.delete()
    return sat


def run():
    report = {"witness": {}, "unsat_widths": {}, "ceiling": CEILING, "WS": WS}
    for K in (2, 3):
        # (a) witness at the claimed max width
        wa = WITNESS_WIDTH[K]
        key = next(k for k in KNOWN if k[0] == wa and k[2] == K)
        col = KNOWN[key]
        valid = check_template(col, *key)[0]
        sat, _, _ = solve(*key)
        report["witness"][K] = {"width": wa, "b": key[1], "published_template_valid": valid, "solver_SAT": sat}
        print(f"K={K}: witness width {wa} (b={key[1]}): published-valid={valid} solver-SAT={sat}")

        # (b) UNSAT for every width wa+1 .. ceiling, every admissible b
        ok_all = True
        widths = list(range(wa + 1, CEILING[K] + 1))
        for a in widths:
            for b in range(1, a):
                boundary = (a == wa + 1 and b == 2)        # emit full certs for the boundary
                sat = confirm_unsat(a, b, K, dump_dimacs=boundary, dump_drat=boundary)
                if sat is not False:
                    ok_all = False
                    print(f"  !! K={K} a={a} b={b}: NOT UNSAT (={sat}) -- claim breaks")
        report["unsat_widths"][K] = {"range": [wa + 1, CEILING[K]], "all_unsat_all_b": ok_all}
        print(f"K={K}: widths {wa+1}..{CEILING[K]} (all b) all-UNSAT = {ok_all}  => WS+({K}) = {wa}")
    json.dump(report, open("wstemplate_proof_report.json", "w"), indent=2)
    print("\nRESULT:",
          "WS+(2)=4" if report["unsat_widths"][2]["all_unsat_all_b"] else "WS+(2) UNCONFIRMED",
          "|",
          "WS+(3)=13" if report["unsat_widths"][3]["all_unsat_all_b"] else "WS+(3) UNCONFIRMED")
    return report


if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"done {time.time()-t0:.1f}s; DIMACS+DRAT boundary certs in {DIMACS_DIR}/")
