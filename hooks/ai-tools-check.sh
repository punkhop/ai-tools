#!/bin/bash
# ai-tools-check.sh — SessionStart hook. Two quiet checks, so a setup left alone for months
# speaks up when it needs a hand instead of failing silently:
#   1. a newer ai-tools release (looked up at most once a week, in the background, never waits
#      on the network), mentioned at most once a week;
#   2. memory search's upkeep job failed its last run.
# Prints nothing when all is well. Changes nothing itself and never blocks a session.

D="$HOME/.claude/ai-tools"; SRC="$D/src"
[ -d "$D" ] || exit 0
cat >/dev/null 2>&1   # the hook input isn't needed

# True when the file is missing or older than N days.
older() { [ ! -f "$1" ] || [ -n "$(find "$1" -mtime +"$2" 2>/dev/null)" ]; }

# 1. Newest release: ask GitHub once a week; the answer lands in newest-version for next time.
if [ -d "$SRC/.git" ] && older "$D/update-checked" 6; then
  touch "$D/update-checked"
  ( GIT_TERMINAL_PROMPT=0 git -C "$SRC" ls-remote --tags --refs --sort=-v:refname origin 'v*' \
      | head -1 | sed 's#.*refs/tags/v##' > "$D/newest-version.tmp" \
      && [ -s "$D/newest-version.tmp" ] && mv "$D/newest-version.tmp" "$D/newest-version" ) \
    </dev/null >/dev/null 2>&1 &
fi
NEW=$(cat "$D/newest-version" 2>/dev/null)
HAVE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("version",""))' "$D/installed.json" 2>/dev/null)
if [ -n "$NEW" ] && [ -n "$HAVE" ] && older "$D/update-told" 6 && python3 -c '
import re, sys
v = lambda s: tuple(int(x) for x in re.findall(r"\d+", s))
sys.exit(0 if v(sys.argv[1]) > v(sys.argv[2]) else 1)' "$NEW" "$HAVE" 2>/dev/null; then
  touch "$D/update-told"
  echo "ai-tools $NEW is out; this computer has $HAVE. At a natural pause, tell the user in one plain line, and that they can say \"check ai-tools for updates\" (the steps: ~/.claude/ai-tools/src/START-HERE.md, section Updates). Never update without them asking."
fi

# 2. Memory search upkeep (only when it is installed).
LAST=$(grep -E '^(ok|FAILED)' /tmp/qmd-upkeep.log 2>/dev/null | tail -1)
case "$LAST" in
  FAILED*) echo "Memory search's upkeep job failed its last run ($LAST; log: /tmp/qmd-upkeep.log). Run ~/.claude/bin/qmd-upkeep upgrade yourself; if it still fails, tell the user in one line and run /doctor." ;;
esac
exit 0
