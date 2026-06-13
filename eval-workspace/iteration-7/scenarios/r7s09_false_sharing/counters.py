# toy model of the production counter layout (C structs simulated):
# 8 worker threads increment adjacent 8-byte counters in one 64-byte array
# (production profile shows 40x slowdown vs per-thread padded counters;
#  perf c2c shows heavy HITM on that cache line)
LAYOUT = "counters[8] packed in a single 64-byte cache line, one per thread"
PERF_NOTES = """
perf c2c report (prod):  cacheline 0x7f3a2c0:  HITM 91%, 8 readers/writers
per-thread throughput: 2.1M ops/s (solo thread: 84M ops/s)
after experiment with thread-local counters + sum-on-read: 78M ops/s/thread
"""
print(LAYOUT); print(PERF_NOTES)
