# Tomorrow 09:00: payments service v3 rollout plan
1. Apply DB schema migration 0042 (adds NOT NULL column `auth_ref` to charges, backfill script included)
2. Deploy v3 to 100% (v3 writes auth_ref; v2 does not know the column)
3. Switch the ledger consumer to the new event format (v3 emits format B; consumer auto-detects)
4. Delete the format-A consumer path "next sprint"
Notes: rollback = redeploy v2. Backfill ETA 40 min for 90M rows. Maintenance
window 09:00-09:30. Queue backlog dashboard exists but has no alert. The
backfill script was tested on staging (2M rows).
Task: review this plan before it ships — what will hurt us and what do we do about it?
