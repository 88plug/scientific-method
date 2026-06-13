# Row-count discrepancy
Before the June 10 storage migration the `events` table reported 5,200 rows
(ops dashboard screenshot, June 9). After migration: 4,000 rows. The pre-
migration snapshot was already rotated, so we "can't know" — but data team
insists the migration dropped 1,200 rows and wants it rolled back.
Facts: the table has a 40-day TTL (rows older than 40 days are purged daily,
see retention.conf). Full post-migration table exported to
after_migration_sample.csv (it IS the whole table). Did the migration drop rows?
