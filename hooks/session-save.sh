#!/usr/bin/env bash
# session-save.sh — SessionEnd hook
#
# At session end, exports the full conversation transcript to
# ~/memory/transcripts/ as searchable markdown. QMD picks it up on
# the next index pass.
#
# Lightweight version — no auto-generated session summaries, no
# project detection. If you want auto-summaries, layer that on later.
#
# Skip gates:
#   1. No transcript file → exit
#   2. < MIN_TURNS assistant turns → trivial session, skip
#
# Failure mode: any error → exit 0, never block session shutdown.

set -uo pipefail

MEMORY_ROOT="$HOME/memory"
TRANSCRIPTS_DIR="$MEMORY_ROOT/transcripts"
MIN_TURNS=5
DATE=$(date +%Y-%m-%d)

mkdir -p "$TRANSCRIPTS_DIR"

INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('transcript_path',''))" 2>/dev/null || true)
SESSION_CWD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null || true)

[ -z "$TRANSCRIPT_PATH" ] && exit 0
[ ! -f "$TRANSCRIPT_PATH" ] && exit 0

# Count assistant turns; skip if trivial
TURN_COUNT=$(python3 -c "
import json, sys
count = 0
with open(sys.argv[1]) as f:
    for line in f:
        try:
            msg = json.loads(line)
            if msg.get('role') == 'assistant' or msg.get('type') == 'assistant':
                count += 1
        except:
            pass
print(count)
" "$TRANSCRIPT_PATH" 2>/dev/null || echo "0")

[ "$TURN_COUNT" -lt "$MIN_TURNS" ] && exit 0

# Derive a stable ID + project tag from cwd
PROJECT=$(basename "${SESSION_CWD:-general}" | tr -c 'a-zA-Z0-9-\n' '_' | tr -d '\n' | head -c 32)
[ -z "$PROJECT" ] && PROJECT="general"

STABLE_ID=$(echo "$TRANSCRIPT_PATH" | md5 -q 2>/dev/null || md5sum <<< "$TRANSCRIPT_PATH" | cut -d' ' -f1)
SHORT_ID="${STABLE_ID:0:8}"

OUTPUT_FILE="$TRANSCRIPTS_DIR/${DATE}-${PROJECT}-${SHORT_ID}.md"

# Dedup — if we already exported this transcript, skip
[ -f "$OUTPUT_FILE" ] && exit 0

# Render the transcript as markdown
python3 - "$TRANSCRIPT_PATH" "$OUTPUT_FILE" "$PROJECT" "$DATE" <<'PY' 2>/dev/null
import json, sys, os

transcript_path, output_path, project, date = sys.argv[1:5]

def extract_text(msg):
    inner = msg.get('message', msg)
    content = inner.get('content', '')
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get('type') == 'text':
                parts.append(p.get('text', ''))
        return ' '.join(parts).strip()
    return str(content).strip()

with open(transcript_path) as f, open(output_path, 'w') as out:
    out.write(f"---\ncreated: {date}\ntype: transcript\nproject: {project}\n---\n\n")
    out.write(f"# Session Transcript: {project} ({date})\n\n")
    for line in f:
        try:
            msg = json.loads(line)
            role = msg.get('type', msg.get('role', ''))
            if role not in ('user', 'assistant'):
                continue
            text = extract_text(msg)
            if not text or len(text) < 5:
                continue
            out.write(f"\n## {role.title()}\n{text}\n")
        except Exception:
            pass
PY

# Trigger QMD reindex if available
QMD_BIN=$(command -v qmd 2>/dev/null || true)
[ -n "$QMD_BIN" ] && "$QMD_BIN" update >/dev/null 2>&1 &

exit 0
