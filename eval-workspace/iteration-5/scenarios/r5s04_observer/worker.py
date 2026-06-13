import sys, threading, time
DEBUG = '--debug' in sys.argv
counter = 0
def log(msg):
    if DEBUG:
        sys.stderr.write(msg+"\n"); sys.stderr.flush(); time.sleep(0.001)
def bump(n):
    global counter
    for _ in range(n):
        log("bump")
        v = counter      # read
        v += 1           # modify
        if not DEBUG: [None]*50  # tiny stall widening the race window in fast mode
        counter = v      # write  (racy read-modify-write)
ts=[threading.Thread(target=bump,args=(20000,)) for _ in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
expected=4*20000
print(f"counter={counter} expected={expected} {'OK' if counter==expected else 'LOST UPDATES'}")
