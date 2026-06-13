# Lost-updates bug
worker.py loses counter updates in prod (run it: "LOST UPDATES"). But when we
add --debug to trace it, it always prints OK — so a teammate concluded "the
debug build is fixed; the race was in the logging path we removed; ship the
debug-style build". Evaluate that conclusion and find the actual bug.
