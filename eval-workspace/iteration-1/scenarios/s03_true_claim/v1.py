import sys
data=open(sys.argv[1]).read()
lines=data.splitlines()  # keeps full copy AND list
total=sum(len(l) for l in lines)
print("v1 total chars:",total)
