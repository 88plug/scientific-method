#!/usr/bin/env bash
# scientific-method plugin — SessionStart hook.
# If a hypothesis ledger (EXPERIMENTS.md) exists for this project, surface it so
# killed hypotheses stay DO-NOT-RE-ATTACK and open predictions survive across
# sessions and compaction. Read-only; silent no-op when no ledger exists.
# For SessionStart, stdout on exit 0 is injected into the session as context.
set -euo pipefail

ledger="${CLAUDE_PROJECT_DIR:-$PWD}/EXPERIMENTS.md"
[ -f "$ledger" ] || exit 0   # no ledger → silent no-op

max=400                       # cap so a large ledger doesn't flood context
total=$(wc -l < "$ledger" | tr -d ' ')

echo "[scientific-method] An active hypothesis ledger exists for this project (EXPERIMENTS.md)."
echo "Honor it: entries in the falsification log are DO-NOT-RE-ATTACK; open hypotheses keep"
echo "their pre-committed predictions; retractions stay struck-through, not deleted."
echo "Run /scientific-method:ledger to update it. Contents follow:"
echo "----------------------------------------"
if [ "$total" -gt "$max" ]; then
  head -n "$max" "$ledger"
  echo "..."
  echo "[truncated: showing first ${max} of ${total} lines — open EXPERIMENTS.md for the rest]"
else
  cat "$ledger"
fi
