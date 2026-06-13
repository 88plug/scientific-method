#!/usr/bin/env python3
"""Regenerate app.log for the r8s05 log-compression scenario.

app.log is a 4.3 MB synthetic, highly-repetitive telemetry corpus — pure eval
fixture, not source. It is git-ignored (so it doesn't ship to every plugin
install) and rebuilt on demand with this deterministic seeded generator. Run:

    python3 gen_app_log.py        # writes ./app.log (60000 lines, ~4.3 MB)

The seed is fixed, so every run produces the identical corpus — the compression
ratios in the scenario's findings are reproducible from this script alone.
Line format:  <ts> <LEVEL> <endpoint> request_id=req-<8hex> latency_ms=<n> status=200
"""
import random
from pathlib import Path

N = 60000
TS0 = 1781300000
LEVELS = (["INFO"] * 80) + (["DEBUG"] * 10) + (["WARN"] * 10)
ENDPOINTS = ["auth", "billing", "search"]
OUT = Path(__file__).resolve().parent / "app.log"


def main() -> None:
    rnd = random.Random(20260613)
    with OUT.open("w") as f:
        for i in range(N):
            ts = TS0 + i
            level = rnd.choice(LEVELS)
            endpoint = rnd.choice(ENDPOINTS)
            rid = f"{rnd.getrandbits(32):08x}"
            latency = rnd.randint(2, 180)
            f.write(f"{ts} {level} {endpoint} request_id=req-{rid} "
                    f"latency_ms={latency} status=200\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {N} lines)")


if __name__ == "__main__":
    main()
