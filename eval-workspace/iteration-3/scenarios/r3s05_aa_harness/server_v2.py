import time,os
base=1000
if os.path.exists("/tmp/.lt_warm"): base=1150
open("/tmp/.lt_warm","w").write("1")
print(base)
