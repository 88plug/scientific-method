import sys, time, hashlib
def work(path):
    t0=time.perf_counter(); h=hashlib.sha256(); n=0
    for line in open(path,'rb'):
        # per-record: parse 3 int fields, hash the line, accumulate
        parts=line.split(b',')
        s=int(parts[0])+int(parts[1])+int(parts[2])
        h.update(line); n+=1
    dt=time.perf_counter()-t0
    print(f"{n} records, digest={h.hexdigest()[:12]}, {n/dt:,.0f} rec/s")
if __name__=='__main__': work(sys.argv[1])
