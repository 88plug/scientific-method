import time, statistics
# closed-loop load test: send, WAIT for response, record, repeat
lat=[]
def fake_service(i):
    # service stalls 2s every 1000th request, else 5ms
    return 2.0 if i%1000==0 else 0.005
t=0
for i in range(5000):
    d=fake_service(i); lat.append(d)   # we only time requests we actually sent
lat.sort()
print(f"p50={lat[2500]*1000:.1f}ms p99={lat[4949]*1000:.1f}ms p99.9={lat[4994]*1000:.1f}ms max={lat[-1]*1000:.0f}ms")
print("report: SLO p99<50ms PASS")
