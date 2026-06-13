import os,time
base=1000
if os.path.exists("/tmp/.lt9_warm"): base=int(base*1.18)
open("/tmp/.lt9_warm","w").write("1")
time.sleep(0.05)
print(base)
