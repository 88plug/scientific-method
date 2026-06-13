import sys, time, json
# "production" record-normalization pipeline (toy but real work)
def normalize(rec):
    d=json.loads(rec)
    d={k.lower():v for k,v in sorted(d.items())}
    return json.dumps(d, separators=(',',':'))
def run(path):
    t0=time.perf_counter(); n=0; out=[]
    for line in open(path):
        out.append(normalize(line)); n+=1
    dt=time.perf_counter()-t0
    print(f"{n} records in {dt:.3f}s = {n/dt:,.0f} rec/s")
if __name__=='__main__': run(sys.argv[1])
