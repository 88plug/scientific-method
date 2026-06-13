import sys, time, argparse, hashlib
ap=argparse.ArgumentParser()
ap.add_argument('--parallel',action='store_true', help='use 4 worker threads')
ap.add_argument('--compress',action='store_true', help='compress payloads')
a=ap.parse_args()
# simulated pipeline: timings model the real system's measured behavior
base=2.0
if a.parallel and not a.compress: t=base*0.55      # parallel helps plain payloads
elif a.parallel and a.compress:   t=base*1.40      # threads contend on the GIL-bound compressor
elif not a.parallel and a.compress: t=base*0.90
else: t=base
time.sleep(t/20)  # scaled-down sleep so runs are fast; printed number is the modeled full-scale time
print(f"parallel={a.parallel} compress={a.compress} pipeline_time={t:.2f}s")
