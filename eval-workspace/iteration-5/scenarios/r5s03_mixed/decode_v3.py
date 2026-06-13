import sys,time
d=open("corpus.txt").read().split("\n")
t0=time.perf_counter()
out=[]
for line in d:
    out.append(line[::-1].strip())
open("out_v3.txt","w").write("\n".join(out))
print(f"v3 {time.perf_counter()-t0:.3f}s")
