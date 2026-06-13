# regenerates data.csv (the reference corpus) — run once before benchmarking
with open("data.csv", "w") as f:
    for i in range(200000):
        f.write(f"{i},Widget Co,2026-01-{(i%28)+1:02d},{i*1.5:.2f}\n")
print("wrote data.csv (200k rows)")
