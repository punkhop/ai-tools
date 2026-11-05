#!/bin/bash
# block-rm-untracked.sh — PreToolUse hook for Bash
#
# Blocks `rm -rf <path>` when any path is untracked in git. Untracked
# files aren't recoverable; this catches accidental work loss.
#
# Allows `rm -rf` on tracked files (git can recover) and on paths outside
# any git repo (no recovery anyway — your call).
#
# Exit 0 = allow
# Exit 2 = block with feedback

command -v jq >/dev/null 2>&1 || exit 0

INPUT=$(cat 2>/dev/null || echo "")
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Only fire on rm -rf (or rm -fr, -Rf, etc.)
echo "$CMD" | grep -qE 'rm\s+(-[a-zA-Z]*[rR]f|-[a-zA-Z]*f[rR]|-rf|-fr|-Rf|-fR)\b' || exit 0

# The paths after each `rm`, up to the end of that command (; && || | and newlines end it),
# so `rm -rf x && find .` checks x, not the `.` that belongs to find.
PATHS=$(echo "$CMD" | python3 -c '
import sys, shlex
for line in sys.stdin.read().splitlines():
  try:
    lex = shlex.shlex(line, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    toks = list(lex)
  except Exception: continue
  in_rm = False
  for t in toks:
    if set(t) <= set(";&|()"):
      in_rm = False
    elif t == "rm":
      in_rm = True
    elif in_rm and not t.startswith("-"):
      print(t)
')

[ -z "$PATHS" ] && exit 0

UNTRACKED_HITS=()
while IFS= read -r p; do
  [ -z "$p" ] && continue
  case "$p" in
    /*) ABS="$p" ;;
    ~/*) ABS="$HOME/${p#~/}" ;;
    *) ABS="$(pwd)/$p" ;;
  esac
  PARENT=$(dirname "$ABS")
  [ ! -d "$PARENT" ] && continue
  # Resolve symlinks (macOS /tmp -> /private/tmp, ~/memory -> the real folder) so the path
  # and git's repo root agree; otherwise the relative path is wrong and nothing is caught.
  PARENT=$(cd "$PARENT" && pwd -P); ABS="$PARENT/$(basename "$ABS")"
  REPO_ROOT=$(cd "$PARENT" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null)
  [ -z "$REPO_ROOT" ] && continue
  REL=$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "$ABS" "$REPO_ROOT")
  STATUS=$(cd "$REPO_ROOT" && git status --porcelain -- "$REL" 2>/dev/null | grep -E '^\?\?')
  if [ -n "$STATUS" ]; then
    UNTRACKED_HITS+=("$ABS")
  fi
done <<< "$PATHS"

if [ ${#UNTRACKED_HITS[@]} -gt 0 ]; then
  cat >&2 <<EOF
BLOCKED: \`rm -rf\` on untracked path(s) — git can't recover these.

Untracked:
$(printf '  - %s\n' "${UNTRACKED_HITS[@]}")

Read each file before deleting, OR move to a tmp directory first.
EOF
  exit 2
fi

exit 0
