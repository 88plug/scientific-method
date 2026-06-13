import random, struct
rng=random.Random(9)
# sensor telemetry: monotonic ~1Hz timestamps with jitter, slowly drifting values
with open("telemetry.csv","w") as f:
    f.write("ts_ms,sensor_id,value\n")
    t=1781400000000; vals={s: rng.uniform(20,30) for s in range(16)}
    for i in range(400000):
        t += rng.choice([999,1000,1000,1000,1001])
        s = i % 16
        vals[s] += rng.uniform(-0.02,0.02)
        f.write(f"{t},{s},{vals[s]:.3f}\n")
print("wrote telemetry.csv")
