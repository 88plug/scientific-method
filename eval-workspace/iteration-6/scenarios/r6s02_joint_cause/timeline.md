# June 3 checkout outage (00:00-00:47)
00:00 TLS cert for payments-gw expired (issued 2025-06-03, 1yr)
00:00 checkout fails closed: cannot reach payments-gw
00:47 cert renewed manually; recovery
Notes:
- A warm fallback path (cached tokenized retry queue) exists EXACTLY for
  gateway outages; it processed zero transactions.
- fallback.conf: enabled=false  # disabled May 12 during the queue migration,
  "re-enable after migration" (migration finished May 20; never re-enabled)
- Cert-expiry alerting: the monitor existed but pointed at the OLD gateway
  hostname since the April DNS cutover; it reported OK throughout.
