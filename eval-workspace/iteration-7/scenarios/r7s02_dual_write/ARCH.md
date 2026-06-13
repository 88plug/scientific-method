# Order service writes
on order update the service does:
  1. UPDATE orders SET ... (postgres, committed)
  2. publish OrderUpdated to kafka (for search index + analytics)
step 2 occasionally fails (network) or the pod dies between 1 and 2.
Result: search shows stale orders ~50x/day. The team proposal: "wrap both in
a try/catch and retry the publish 5 times." Evaluate and recommend.
