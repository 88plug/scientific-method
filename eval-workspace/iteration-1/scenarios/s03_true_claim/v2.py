import sys
total=0
with open(sys.argv[1]) as f:
    for line in f:  # streaming, one line at a time
        total+=len(line.rstrip("\n"))
print("v2 total chars:",total)
