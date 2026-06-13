import sys, time, hashlib, argparse
ap=argparse.ArgumentParser()
ap.add_argument('file'); ap.add_argument('--algo',default='sha256',choices=['sha256','blake2b'])
a=ap.parse_args()
t0=time.perf_counter()
data=open(a.file,'rb').read()
load=time.perf_counter()-t0
t1=time.perf_counter()
h=hashlib.new(a.algo); h.update(data)
print(f"{a.algo} {h.hexdigest()[:16]} load={load:.3f}s hash={time.perf_counter()-t1:.3f}s total={time.perf_counter()-t0:.3f}s")
