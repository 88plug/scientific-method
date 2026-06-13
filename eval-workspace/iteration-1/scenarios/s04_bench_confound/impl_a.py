import sys, json, time, collections
# builds index.json then queries it
if '--build-index' in sys.argv:
    c=collections.Counter()
    with open('words.txt') as f:
        for line in f: c[line.strip()]+=1
    json.dump(c, open('index.json','w')); print("index built")
else:
    idx=json.load(open('index.json'))
    t0=time.perf_counter()
    s=sum(v for k,v in idx.items() if k.startswith('q'))
    print(f"A query: {s} in {time.perf_counter()-t0:.4f}s")
