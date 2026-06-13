# test_checkout_flow flakiness
Flaked 0 times in May. Flaked 4 times June 2-8. Commit a41f9c2 ("switch to
async session pool") merged June 1. CI provider purges logs after 72h — runs
before June 9 have no logs. Since June 9 (after we pinned the pool size as a
guess) zero flakes in 60 runs.
Question for the retro: did a41f9c2 cause the flakes? Definitive answer needed.
