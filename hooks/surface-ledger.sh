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
if [ "$total" -le "$max" ]; then
  cat "$ledger"
  exit 0
fi

# Large ledger: head alone hid DO-NOT-RE-ATTACK / falsification near the file end.
# Always surface head (active hypotheses) + any kill-log section + tail.
head_n=240
tail_n=100

head -n "$head_n" "$ledger"
echo "..."

# Extract from first matching kill/falsification heading to next top-level heading or EOF
kill_block=$(
  awk '
    BEGIN { IGNORECASE=1 }
    /^#{1,3}[[:space:]]*(Falsification|DO[- ]?NOT[- ]?RE[- ]?ATTACK|Kill[[:space:]]+log|Killed)/ {
      grab=1
    }
    grab {
      if (/^#{1,3}[[:space:]]/ && !/Falsification|DO[- ]?NOT|Kill[[:space:]]+log|Killed/ && printed) {
        exit
      }
      print
      printed=1
    }
  ' "$ledger" 2>/dev/null || true
)

if [ -n "$(printf '%s' "$kill_block" | tr -d '[:space:]')" ]; then
  echo "[scientific-method] Falsification / DO-NOT-RE-ATTACK section (always included):"
  printf '%s\n' "$kill_block"
else
  echo "[scientific-method] Ledger tail (may include kill log):"
  tail -n "$tail_n" "$ledger"
fi
echo "[truncated: ledger has ${total} lines — open EXPERIMENTS.md for the full file]"
