import sys
from collections import OrderedDict
def lru(trace, cap):
    c=OrderedDict(); hits=0
    for k in trace:
        if k in c: hits+=1; c.move_to_end(k)
        else:
            if len(c)>=cap: c.popitem(last=False)
            c[k]=1
    return hits
if __name__=='__main__':
    tr=[int(l) for l in open('trace.txt')]
    cap=int(sys.argv[1]) if len(sys.argv)>1 else 100
    h=lru(tr,cap); print(f"LRU cap={cap}: hit rate {h/len(tr)*100:.2f}%")
