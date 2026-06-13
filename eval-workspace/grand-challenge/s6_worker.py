import sys, time, json
sys.path.insert(0,'verifiers')
from verify import verify_schur
import schur_sat2 as M
N=int(sys.argv[1]); wid=int(sys.argv[2])
# diversify by assigning a small spread of "anchor" integers to colors derived from worker id (base-6 digits)
# anchors chosen in the mid/high range where structure is tight; pure search-space split, sound (just fixes some vars)
anchors=[150, 300, 450]
prefix={}
w=wid
for a in anchors:
    prefix[a]= w % 6; w//=6
sat,col,dt=M.solve(N,6,prefix=prefix)
if sat:
    ok,d=verify_schur(6,col,weak=False)
    if ok:
        json.dump(col,open(f'found_S6_{N}.json','w'))
        print(f"WORKER {wid} SAT+VERIFIED {d} in {dt:.0f}s prefix={prefix}", flush=True)
    else:
        print(f"WORKER {wid} SAT-but-INVALID(!) {d}", flush=True)
else:
    print(f"worker {wid} unsat {dt:.0f}s prefix={prefix}", flush=True)
