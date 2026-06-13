#!/bin/bash
set -e
# documented rollback: restore the v1 snapshot then flip the symlink
tar -xzf backups/v1_snapshot_2026-04-01.tgz -C live/
ln -sfn live/v1 current
echo "rollback complete"
