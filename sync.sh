#!/usr/bin/env bash
# Send experiments and results to GitHub, and get anyone else's: ./sync.sh "optional message"
# Never sends keys: keys.env and data/config.json are ignored by git.
set -euo pipefail
cd "$(dirname "$0")"
for f in data/runs/*/items.jsonl; do
  [ -f "$f" ] || continue
  [ "$f.gz" -nt "$f" ] || gzip -n -c "$f" > "$f.gz"
done
git add experiments practices data prereg 2>/dev/null || true
if git diff --cached --quiet; then
  echo "Nothing new to send."
else
  git commit -q -m "${1:-Sync experiments and results $(date +%Y-%m-%d)}"
  echo "Committed."
fi
git pull -q --rebase
git push -q
echo "Synced with GitHub."
