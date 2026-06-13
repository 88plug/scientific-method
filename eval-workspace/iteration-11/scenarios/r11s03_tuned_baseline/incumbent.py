import sys, time, json
# incumbent JSON-lines filter: keeps records where score >= threshold
# SHIPPED CONFIG (config.json): batch_size=1 (pathological default)
def run(path, batch_size=1):
    t0=time.perf_counter(); kept=0; batch=[]
    for line in open(path):
        batch.append(line)
        if len(batch)>=batch_size:
            for l in batch:
                if json.loads(l)["score"]>=50: kept+=1
            batch=[]
    for l in batch:
        if json.loads(l)["score"]>=50: kept+=1
    dt=time.perf_counter()-t0
    print(f"kept={kept} time={dt:.3f}s")
    return dt
if __name__=='__main__':
    import json as j
    cfg=j.load(open('config.json'))
    run(sys.argv[1], cfg.get('batch_size',1))
