import threading
# the racy worker from prior campaigns: 4 threads, read-modify-write
counter=0
def bump(n):
    global counter
    for _ in range(n):
        v=counter; v+=1; counter=v
def run(n=5000, threads=4):
    global counter; counter=0
    ts=[threading.Thread(target=bump,args=(n,)) for _ in range(threads)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return counter, n*threads
