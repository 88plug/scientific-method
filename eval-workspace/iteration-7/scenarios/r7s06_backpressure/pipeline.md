# Ingest pipeline
producer (bursty, up to 50k msg/s) -> in-memory unbounded queue -> consumer
(steady 8k msg/s) -> sink.
Symptom: during campaigns the worker RSS climbs for ~20 min then OOM-kills;
after restart it crash-loops while the producer is still bursting.
Proposal on the table: "double the worker memory."
Evaluate and recommend.
