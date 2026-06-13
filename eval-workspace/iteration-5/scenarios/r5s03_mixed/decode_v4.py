import sys,time
d=open("corpus.txt").read().split("\n")
t0=time.perf_counter()
out=[l[::-1].strip() for l in d]
open("out_v4.txt","w").write("\n".join(out))
print(f"v4 {time.perf_counter()-t0:.3f}s")
