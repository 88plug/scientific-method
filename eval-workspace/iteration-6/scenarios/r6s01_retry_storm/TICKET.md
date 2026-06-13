# 25-minute brownout at 14:20
Incoming traffic was FLAT at ~1000 rps the whole time, every component passed
its health checks and met spec, yet total load hit 5x and timeouts 60%. The
v9.4.1 deploy at 14:18 is suspected (2 min before!). Root cause this and
propose the fix.
