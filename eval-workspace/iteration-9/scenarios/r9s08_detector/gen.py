import random, math
rng=random.Random(17)
# 4 weeks of per-minute request latency p50; daily seasonality + noise;
# 5 planted incidents (sustained 3-8x elevation, 8-25 min each)
incidents=[(2900,12),(9400,25),(17800,8),(26500,15),(36100,20)]
with open("metric.csv","w") as f:
    f.write("minute,p50_ms\n")
    for m in range(40320):
        base=40+18*math.sin(2*math.pi*(m%1440)/1440)
        v=base+rng.gauss(0,4)
        for s,d in incidents:
            if s<=m<s+d: v=base*rng.uniform(3,8)
        if rng.random()<0.0008: v=base*rng.uniform(2.5,4)   # 1-minute blips (NOT incidents)
        f.write(f"{m},{v:.1f}\n")
print("ok; incidents at minutes:", incidents)
