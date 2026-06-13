# June 7 outage timeline (08:00-08:40)
07:55 config push: conn_timeout 5s -> 0.5s (all api pods)
08:00 traffic shifts: partner batch job starts (3x request rate, runs daily)
08:02 api error rate 0.1% -> 31%
08:25 config reverted; errors drop to 0.4% by 08:30
08:31 partner batch still running until 09:10; errors stay ~0.4%
Note: the partner batch has run daily for months without incident.
Note: the 0.5s timeout was previously tested in staging (low traffic) fine.
