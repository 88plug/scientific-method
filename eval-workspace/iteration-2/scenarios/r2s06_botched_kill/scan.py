import sys, time, argparse, mmap
ap=argparse.ArgumentParser()
ap.add_argument('--mode',choices=['mmap','buf','map'],default='buf')
ap.add_argument('file')
a=ap.parse_args()
t0=time.perf_counter(); total=0
if a.mode=='mmap':
    with open(a.file,'rb') as f:
        m=mmap.mmap(f.fileno(),0,prot=mmap.PROT_READ)
        total=sum(m[i] for i in range(0,len(m),4096))
elif a.mode=='map':   # legacy alias: falls back to BYTE-BY-BYTE python loop (slow path)
    with open(a.file,'rb') as f:
        data=f.read()
        for i in range(0,len(data),1):
            if i%4096==0: total+=data[i]
else:
    with open(a.file,'rb') as f:
        data=f.read()
        total=sum(data[i] for i in range(0,len(data),4096))
print(f"mode={a.mode} sum={total} t={time.perf_counter()-t0:.2f}s")
