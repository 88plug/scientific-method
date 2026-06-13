import itertools
from wstemplate_sat import solve, check_template, build
from pysat.solvers import Cadical195

def all_valid_bruteforce(a,b,K):
    N=a+b; valid=[]
    for assign in itertools.product(range(1,K+1), repeat=N):
        col={i+1:assign[i] for i in range(N)}
        if check_template(col,a,b,K)[0]:
            valid.append(col)
    return valid

def all_sat_models(a,b,K):
    cnf,var,N=build(a,b,K)
    s=Cadical195(bootstrap_with=cnf.clauses)
    models=[]
    while s.solve():
        m=set(l for l in s.get_model() if l>0)
        col={x:c for x in range(1,N+1) for c in range(1,K+1) if var(x,c) in m}
        models.append(col)
        s.add_clause([-var(x,col[x]) for x in range(1,N+1)])  # block
    s.delete()
    return models

for (a,b,K) in [(4,2,2),(5,2,2),(4,3,2),(6,3,2),(13,8,3) if False else (7,3,2)]:
    bf=all_valid_bruteforce(a,b,K)
    sat=all_sat_models(a,b,K)
    bf_set={tuple(sorted(c.items())) for c in bf}
    sat_set={tuple(sorted(c.items())) for c in sat}
    print(f"(a={a},b={b},K={K}): checker-valid={len(bf_set)}  solver-models={len(sat_set)}  IDENTICAL={bf_set==sat_set}")
