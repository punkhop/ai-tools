#!/bin/bash
# context-budget-feedback.sh — UserPromptSubmit hook
#
# Claude can't see how full its own context window is. This hook reads the thread's own
# transcript (hook input carries `transcript_path`), takes the last assistant turn's usage
# (input + cache_read + cache_creation = the live context size) and injects the position
# as `additionalContext` — but ONLY when the size crosses UP into a new zone (hysteresis),
# so turns under the first line stay silent and we don't pollute the context we protect.
#
# Why the transcript: every launcher writes it (terminal, desktop apps, headless runs), so
# this works everywhere. A terminal statusline file is kept as a fallback when the
# transcript can't be read.
#
# Thresholds are TOKENS, not percent: on a 1M window "60%" means 600k. A model reasons
# best early; answers degrade well before the window is full, whatever its size.
# 150k = send wide reads to subagents; 250k = build work hands off to a fresh session at
# the next natural break, while a thread the user is talking with carries on.
#
# Fail-open in every branch: missing/stale/null data -> exit 0, inject nothing.
# Never blocks the prompt.

command -v jq >/dev/null 2>&1 || exit 0

INPUT=$(cat 2>/dev/null || echo "")
SID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
[ -z "$SID" ] && exit 0
TRANSCRIPT=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)

TOKENS=0
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  # Last assistant usage in the tail of the file (the transcript can be many MB; the last 400
  # LINES always hold the last turn — line-based, so no half-line breaks jq). Sidechain
  # (subagent) lines are excluded.
  TOKENS=$(tail -n 400 "$TRANSCRIPT" 2>/dev/null \
    | jq -r 'select(.type=="assistant" and (.isSidechain|not) and .message.usage)
             | .message.usage
             | ((.input_tokens // 0) + (.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0))' 2>/dev/null \
    | tail -1)
  TOKENS=${TOKENS:-0}
fi

# Fallback: a terminal statusline's bridge file, if one writes it ({"tokens": N, "ts": epoch}).
if ! [ "$TOKENS" -gt 0 ] 2>/dev/null; then
  CTX_FILE="${TMPDIR:-/tmp}/claude-ctx/$SID.json"
  if [ -f "$CTX_FILE" ]; then
    T=$(jq -r '.tokens // 0' "$CTX_FILE" 2>/dev/null); T=${T%%.*}
    TS=$(jq -r '.ts // 0' "$CTX_FILE" 2>/dev/null)
    NOW=$(date +%s)
    if [ "${TS:-0}" -gt 0 ] 2>/dev/null && [ $((NOW - TS)) -le 30 ] && [ "${T:-0}" -gt 0 ] 2>/dev/null; then
      TOKENS=$T
    fi
  fi
fi
[ "$TOKENS" -gt 0 ] 2>/dev/null || exit 0

# --- thresholds (tokens) ---
Y=150000; O=250000   # offload · build threads hand off at a break

LEVEL=0
if   [ "$TOKENS" -ge "$O" ]; then LEVEL=2
elif [ "$TOKENS" -ge "$Y" ]; then LEVEL=1
fi

# --- hysteresis: only speak on escalation; always record current so a drop (a fresh session) re-arms ---
CTX_DIR="${TMPDIR:-/tmp}/claude-ctx"
mkdir -p "$CTX_DIR" 2>/dev/null || true
ZONE_FILE="$CTX_DIR/$SID.zone"
PREV=0
[ -f "$ZONE_FILE" ] && PREV=$(cat "$ZONE_FILE" 2>/dev/null || echo 0)
printf '%s' "$LEVEL" > "$ZONE_FILE" 2>/dev/null || true
[ "$LEVEL" -le "$PREV" ] && exit 0   # no upward crossing -> silent
[ "$LEVEL" -eq 0 ] && exit 0

K=$((TOKENS / 1000))
MSG=""
case "$LEVEL" in
  1) MSG="Context is ${K}k tokens — past 150k, where reasoning starts to slip. Do not hand off yet: keep talking with the user, but send any wide read or big output to a subagent and keep only its conclusion here. Don't re-read files already in this conversation." ;;
  2) MSG="Context is ${K}k tokens — past 250k. Build work running on its own: hand off at the next natural break (run /pass if it is installed; otherwise tell the user it's a good moment to start a fresh session and write them a short handoff). Talking with the user (questions, discussion, design): do not hand off — carry on; Claude Code compacts the thread on its own when it fills up." ;;
esac
[ -z "$MSG" ] && exit 0

jq -n --arg m "$MSG" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:$m}}' 2>/dev/null || true
exit 0
