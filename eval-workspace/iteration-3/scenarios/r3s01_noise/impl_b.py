import time,random,sys
random.seed()
t=0.49*(1+random.uniform(-0.08,0.08))
time.sleep(t)
print(f"B done in {t:.3f}s")
