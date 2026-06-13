import sys, time
sys.path.insert(0, '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge/verifiers')
sys.path.insert(0, '/home/andrew/scientific-method-plugin/eval-workspace/grand-challenge')
from verify import verify_schur
import schur_sym as M

print("[gate] symmetric S(4)[1,44] correctness ...", flush=True)
sat, col, dt = M.solve(44, 4)
print(f"[gate] S(4)[1,44]: {'SAT' if sat else 'UNSAT'} {dt:.1f}s "
      f"{'verif=' + str(verify_schur(4, col, weak=False)[0]) if sat else ''}", flush=True)

print("[gate] symmetric S(5)[1,160] feasibility (make-or-break signal) ...", flush=True)
sat, col, dt = M.solve(160, 5)
print(f"[gate] S(5)[1,160]: {'SAT' if sat else 'UNSAT'} {dt:.1f}s "
      f"{'verif=' + str(verify_schur(5, col, weak=False)[0]) if sat else ''}", flush=True)
