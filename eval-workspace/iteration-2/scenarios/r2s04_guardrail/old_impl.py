import sys, time
def process(path):
    t0=time.perf_counter(); total=0
    with open(path) as f:
        for line in f: total+=int(line)
    return total, time.perf_counter()-t0
if __name__=="__main__":
    tot,dt=process(sys.argv[1]); print(f"old total={tot} time={dt:.3f}s")
