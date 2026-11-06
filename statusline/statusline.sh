#!/bin/bash
# statusline.sh — the two lines under the prompt in Claude Code in a terminal.
#   Line 1: the folder Claude is working in, and its git branch.
#   Line 2: how full this chat is — a bar that turns yellow at 70% and red at 90%.
# Claude Code runs it after each reply and hands it the session as JSON on stdin.
# Needs jq. Mac and Linux. Also leaves the chat's size in a small file that the
# safety nets' long-thread warning can read when it can't read the transcript.

input=$(cat)
command -v jq >/dev/null 2>&1 || { echo "status bar needs jq"; exit 0; }

eval "$(printf '%s' "$input" | jq -r '
  @sh "DIR=\(.workspace.current_dir // .cwd // "")",
  @sh "PCT=\(.context_window.used_percentage // 0)",
  @sh "SID=\(.session_id // "")",
  @sh "TOKENS=\(.context_window.total_input_tokens // .context_window.current_usage.input_tokens // 0)"
')"
PCT=${PCT%%.*}; [ "$PCT" -ge 0 ] 2>/dev/null || PCT=0; [ "$PCT" -gt 100 ] && PCT=100

# The chat's size for the long-thread warning (one small file per chat, never fatal).
if [ -n "$SID" ] && [ "$PCT" -gt 0 ]; then
  CTX_DIR="${TMPDIR:-/tmp}/claude-ctx"
  mkdir -p "$CTX_DIR" 2>/dev/null \
    && printf '{"pct":%s,"tokens":%s,"session_id":"%s","ts":%s}\n' "$PCT" "${TOKENS%%.*}" "$SID" "$(date +%s)" \
      > "$CTX_DIR/$SID.json.tmp" 2>/dev/null \
    && mv -f "$CTX_DIR/$SID.json.tmp" "$CTX_DIR/$SID.json" 2>/dev/null
fi

# Line 1: folder and branch.
LINE1=$(basename "${DIR:-$PWD}")
BRANCH=$(git -C "${DIR:-$PWD}" branch --show-current 2>/dev/null)
[ -n "$BRANCH" ] && LINE1="$LINE1 · $BRANCH"

# Line 2: the bar.
if [ "$PCT" -ge 90 ]; then COLOR='\033[31m'
elif [ "$PCT" -ge 70 ]; then COLOR='\033[33m'
else COLOR='\033[32m'; fi
WIDTH=20; FILLED=$((PCT * WIDTH / 100))
printf -v FULL '%*s' "$FILLED" ''; printf -v REST '%*s' "$((WIDTH - FILLED))" ''
BAR="${FULL// /█}${REST// /░}"

printf '%b\n' "\033[36m${LINE1}\033[0m"
printf '%b\n' "${COLOR}${BAR}\033[0m ${PCT}% of this chat"
