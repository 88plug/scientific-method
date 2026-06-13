import sys, time
def process(path):
    t0=time.perf_counter()
    nums=[int(x) for x in open(path).read().split()]  # slurp whole file
    lookup=dict(enumerate(nums))                       # extra index "for future features"
    total=sum(nums)
    return total, time.perf_counter()-t0
if __name__=="__main__":
    tot,dt=process(sys.argv[1]); print(f"new total={tot} time={dt:.3f}s")
