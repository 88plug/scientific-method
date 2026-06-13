import threading
counter=0
def bump(n):
    global counter
    for _ in range(n):
        v=counter; v+=1; [None]*30; counter=v
ts=[threading.Thread(target=bump,args=(20000,)) for _ in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
print(f"counter={counter} expected=80000 {'OK' if counter==80000 else 'LOST'}")
