import sys,time
rows=0
for line in open(sys.argv[1]):
    parts=line.split(",")
    if len(parts)==3: rows+=1
    time.sleep(0)  
print(f"old rows={rows}")
