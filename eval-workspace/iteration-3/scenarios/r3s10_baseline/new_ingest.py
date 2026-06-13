import sys
data=open(sys.argv[1]).read().splitlines()
rows=sum(1 for l in data if l.count(",")==2)
print(f"new rows={rows}")
