#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
PY="${PYTHON:-python3}"

echo "=== smoke: manifest JSON valid ==="
"$PY" -c "import json; json.load(open('.claude-plugin/plugin.json')); print('  ok: .claude-plugin/plugin.json')"
"$PY" -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('  ok: .claude-plugin/marketplace.json')" 2>/dev/null || echo "  skip: no marketplace.json"
"$PY" -c "import json; json.load(open('hooks/hooks.json')); print('  ok: hooks/hooks.json')"

echo "=== smoke: keywords == 20 ==="
"$PY" -c "import json; k=json.load(open('.claude-plugin/plugin.json')).get('keywords',[]); assert len(k)==20, f'keywords={len(k)} (want 20)'; print('  ok: 20 keywords')"

echo "=== smoke: hook bash syntax ==="
find hooks/ -name "*.sh" | while read -r f; do
    bash -n "$f" && echo "  ok: $f"
done

echo "=== smoke: all good ==="
