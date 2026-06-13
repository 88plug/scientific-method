import json, time
idx=json.load(open('index.json'))
t0=time.perf_counter()
s=sum(v for k,v in idx.items() if k.startswith('q'))
print(f"B query: {s} in {time.perf_counter()-t0:.4f}s")
