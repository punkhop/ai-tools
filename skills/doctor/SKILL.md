---
name: doctor
description: Health check of this Claude Code setup — checks only the pieces you installed (listed in ~/.claude/ai-tools/installed.json) — memory folder, skills, hooks, memory search, the file server, Tailscale, Syncthing, the Development Bible, the codex CLI. Mac and Linux. Prints OK / WARN / FAIL with a one-line fix for each. Use after install, when something feels off, or when memory search or links stop working.
disable-model-invocation: false
---

# /doctor — health check

Checks only what is installed. The installer writes `~/.claude/ai-tools/installed.json`:

```json
{"version": "1.0.0", "installed_at": "...", "pieces": {"<piece-id>": {"version": "1.0.0", "files": ["..."]}}}
```

Run step 0, then step 1, then the section for **each piece listed** in step 0 — skip the sections
for pieces that aren't listed, without mentioning them. One Bash call per section; show each result
as it comes. Then print the summary and fix what you can (see **After the checks**).

Every check prints one line starting `OK`, `WARN` or `FAIL`, followed by the fix when it isn't OK.
FAIL = something the user relies on is broken. WARN = degraded, optional, or not yet proven.

Put this header at the top of every Bash call (shell state doesn't carry between calls):

```bash
OS=$(uname -s)   # Darwin = Mac, Linux = Linux
M=~/.claude/ai-tools/installed.json
S=~/.claude/settings.json
export PATH="$HOME/.local/bin:$HOME/.claude/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
mtime() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1"; }
registered() { grep -q "$1" "$S" 2>/dev/null && echo "OK $1 registered in settings.json" || echo "FAIL $1 not in settings.json — rerun the installer and pick this piece again"; }
runnable() { [ -x ~/.claude/hooks/$1 ] && echo "OK $1 executable" || echo "FAIL $1 missing or not executable — chmod +x ~/.claude/hooks/$1 (missing: rerun the installer)"; }
```

## 0. What is installed

```bash
python3 - "$M" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1]))
except FileNotFoundError:
    print(f"FAIL {sys.argv[1]} missing — nothing was installed with the installer; run it first"); sys.exit()
except Exception as error:
    print(f"FAIL {sys.argv[1]} is not valid JSON ({error}) — rerun the installer"); sys.exit()
pieces = data.get("pieces") or {}
print(f"OK ai-tools {data.get('version', '?')}, installed {data.get('installed_at', '?')}")
print("PIECES " + " ".join(sorted(pieces)))
PY
```

The `PIECES` line is the list of sections to run. If step 0 FAILs, stop and tell the user to run the installer.

## 1. Every installed file is present

```bash
python3 - "$M" <<'PY'
import json, os, sys
pieces = json.load(open(sys.argv[1])).get("pieces") or {}
home = os.path.expanduser("~")
for piece_id, piece in sorted(pieces.items()):
    missing = []
    for path in piece.get("files") or []:
        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.join(home, ".claude", path)
        if not os.path.exists(path):
            missing.append(path)
    if missing:
        print(f"FAIL {piece_id}: {len(missing)} file(s) missing, e.g. {missing[0]} — rerun the installer and pick {piece_id}")
    else:
        print(f"OK {piece_id} {piece.get('version', '?')}: all {len(piece.get('files') or [])} file(s) present")
PY
python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$S" 2>/dev/null \
  && echo "OK settings.json is valid JSON" || echo "FAIL ~/.claude/settings.json missing or broken JSON — Claude ignores all of it; rerun the installer"
```

## memory

```bash
if [ -L ~/memory ]; then REAL=$(cd ~/memory 2>/dev/null && pwd -P)
  [ -n "$REAL" ] && [ -d "$REAL" ] && echo "OK ~/memory → $REAL" || echo "FAIL ~/memory points at a missing folder — start the sync app or mount the drive"
elif [ -d ~/memory ]; then echo "OK ~/memory is the memory folder"
else echo "FAIL ~/memory missing — mkdir -p ~/memory/{sessions,handoffs,transcripts}"; fi
for d in sessions handoffs transcripts; do
  [ -d ~/memory/$d ] && echo "OK ~/memory/$d" || echo "FAIL ~/memory/$d missing — mkdir -p ~/memory/$d"
done
[ -w ~/memory/sessions ] && echo "OK memory is writable" || echo "FAIL can't write to ~/memory/sessions — check the folder's owner and permissions"
```

## note

```bash
[ -f ~/.claude/skills/note/SKILL.md ] && echo "OK /note" || echo "FAIL /note missing — rerun the installer and pick note"
[ -w ~/memory/sessions ] && echo "OK notes have somewhere to go" || echo "FAIL ~/memory/sessions missing or read-only — mkdir -p ~/memory/sessions"
```

## session-save

```bash
registered session-save.sh; runnable session-save.sh
LATEST=$(ls -t ~/memory/transcripts/*.md 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then AGE=$(( ($(date +%s) - $(mtime "$LATEST")) / 86400 ))
  [ "$AGE" -lt 7 ] && echo "OK newest transcript $AGE day(s) old" || echo "WARN newest transcript is $AGE days old — fine if Claude wasn't used; else check the session-save hook"
else echo "WARN no transcripts yet — normal on a fresh install (sessions under 5 replies are skipped)"; fi
```

## safety-hooks

```bash
registered block-secrets.py; registered block-rm-untracked.sh; runnable block-rm-untracked.sh
[ -f ~/.claude/hooks/block-secrets.py ] && echo "OK block-secrets.py present" || echo "FAIL block-secrets.py missing — rerun the installer and pick safety-hooks"
command -v jq >/dev/null && echo "OK jq (the rm guard needs it)" || echo "FAIL jq missing — the rm guard silently does nothing (Mac: brew install jq · Linux: install jq with your package manager)"
echo '{"tool_input":{"file_path":"/x/.env"}}' | python3 ~/.claude/hooks/block-secrets.py 2>/dev/null
[ $? -eq 2 ] && echo "OK secrets guard blocks .env files" || echo "FAIL secrets guard let a .env file through — rerun the installer and pick safety-hooks"
T=$(mktemp -d); (cd "$T" && git init -q && touch scratch.txt)
printf '{"tool_input":{"command":"rm -rf %s/scratch.txt"}}' "$T" | ~/.claude/hooks/block-rm-untracked.sh 2>/dev/null
[ $? -eq 2 ] && echo "OK rm guard blocks deleting untracked files" || echo "FAIL rm guard let an untracked file be deleted — check jq is installed, then rerun the installer"
rm -r "$T"
```

## dev-bible

```bash
B=~/.claude/ai-tools/bibles/01-DEVELOPMENT-BIBLE.md
[ -f "$B" ] && echo "OK Development Bible present" || echo "FAIL $B missing — rerun the installer and pick dev-bible"
grep -qE '^@.*ai-tools/bibles/01-DEVELOPMENT-BIBLE\.md' ~/.claude/CLAUDE.md 2>/dev/null \
  && echo "OK the bible loads in every session (imported in ~/.claude/CLAUDE.md)" \
  || echo "FAIL the bible isn't imported — add this line to ~/.claude/CLAUDE.md: @~/.claude/ai-tools/bibles/01-DEVELOPMENT-BIBLE.md"
```

## chat-voice, plain-voice

Run once per voice piece that is listed (replace `chat-voice` with the piece id):

```bash
P=chat-voice
python3 - "$M" "$P" <<'PY'
import json, os, re, sys
pieces = json.load(open(sys.argv[1])).get("pieces") or {}
files = [f for f in (pieces.get(sys.argv[2]) or {}).get("files") or [] if f.endswith(".md") and "/skills/" not in f]
try:
    claude_md = open(os.path.expanduser("~/.claude/CLAUDE.md")).read()
except OSError:
    claude_md = ""
names = [os.path.basename(f) for f in files]
if not names:
    print(f"OK {sys.argv[2]}: no rule files to import")
elif any(re.search(r"^@.*" + re.escape(n), claude_md, re.M) for n in names):
    print(f"OK {sys.argv[2]} rules load in every session (imported in ~/.claude/CLAUDE.md)")
else:
    print(f"WARN {sys.argv[2]} rules aren't imported in ~/.claude/CLAUDE.md — rerun the installer and pick {sys.argv[2]}")
PY
```

## html

The file check in step 1 covers it. Nothing more to run.

## pass-handoff

```bash
for s in pass handoff; do
  [ -f ~/.claude/skills/$s/SKILL.md ] && echo "OK /$s" || echo "FAIL /$s missing — rerun the installer and pick pass-handoff"
done
[ -d ~/memory/handoffs ] && echo "OK ~/memory/handoffs" || echo "FAIL ~/memory/handoffs missing — mkdir -p ~/memory/handoffs"
registered context-budget-feedback.sh; runnable context-budget-feedback.sh
command -v jq >/dev/null && echo "OK jq (the context-size warning needs it)" || echo "WARN jq missing — Claude gets no warning when a thread grows long (Mac: brew install jq · Linux: install jq)"
```

## qmd

```bash
if command -v qmd >/dev/null; then echo "OK $(qmd --version)"
  node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' 2>/dev/null \
    && echo "OK node $(node --version)" || echo "FAIL node $(node --version 2>/dev/null) — QMD needs Node 22 or newer"
  ST=$(qmd status 2>/dev/null)
  UPD=$(printf '%s\n' "$ST" | grep -m1 'Updated:' | sed 's/.*Updated: *//')
  case "$UPD" in
    "") if printf '%s\n' "$ST" | grep -qE 'Total: +0 files'; then
          echo "WARN index is empty — normal until the first note; run ~/.claude/bin/qmd-upkeep index after writing one"
        else echo "FAIL qmd status doesn't answer — run ~/.claude/bin/qmd-upkeep upgrade (a Node upgrade breaks it)"; fi ;;
    never*) echo "FAIL index never built — qmd update && qmd embed" ;;
    *s\ ago|*m\ ago|1h\ ago|2h\ ago) echo "OK index updated $UPD" ;;
    *) echo "WARN index last updated $UPD — the 30-minute upkeep job isn't running (see below)" ;;
  esac
  qmd collection list 2>/dev/null | grep -q '^memory ' && echo "OK collection 'memory'" \
    || echo "FAIL no 'memory' collection — qmd collection add \"\$(cd ~/memory && pwd -P)\" --name memory"
else echo "FAIL qmd not installed — npm install -g @tobilu/qmd"; fi
OUT=$(claude mcp list 2>&1 | grep -i '^qmd')
case "$OUT" in
  *onnected*) echo "OK qmd connected to Claude" ;;
  "") echo "FAIL qmd not registered with Claude — rerun the installer and pick qmd, then restart Claude" ;;
  *) echo "FAIL qmd registered but not connecting: $OUT — run qmd mcp by hand to see the error" ;;
esac
if [ "$OS" = Darwin ]; then
  for j in com.user.qmd-index com.user.qmd-upgrade; do
    launchctl list | grep -q "$j" && echo "OK $j loaded" || echo "FAIL $j not loaded — launchctl load -w ~/Library/LaunchAgents/$j.plist"
  done
else
  for t in qmd-index qmd-upgrade; do
    systemctl --user is-active --quiet $t.timer && echo "OK $t.timer active" || echo "FAIL $t.timer not active — systemctl --user enable --now $t.timer"
  done
  loginctl show-user "$USER" -p Linger 2>/dev/null | grep -q yes && echo "OK linger on (jobs run while logged out)" \
    || echo "WARN linger off — jobs stop when you log out: loginctl enable-linger $USER"
fi
[ -x ~/.claude/bin/qmd-upkeep ] && echo "OK qmd-upkeep installed" || echo "FAIL ~/.claude/bin/qmd-upkeep missing — rerun the installer and pick qmd"
LAST=$(grep -E '^(ok|FAILED)' /tmp/qmd-upkeep.log 2>/dev/null | tail -1)
case "$LAST" in
  ok) echo "OK last upkeep run ok" ;;
  FAILED*) echo "FAIL last upkeep run: $LAST — see tail -30 /tmp/qmd-upkeep.log" ;;
  *) echo "WARN no upkeep runs logged yet (the log clears on restart) — wait 30 minutes or run ~/.claude/bin/qmd-upkeep index" ;;
esac
```

## tailscale

```bash
TS=$(command -v tailscale || echo /Applications/Tailscale.app/Contents/MacOS/Tailscale)
"$TS" status >/dev/null 2>&1 && echo "OK Tailscale up" \
  || echo "FAIL Tailscale down — links won't open on other devices (Mac: open the Tailscale app and connect · Linux: sudo tailscale up)"
```

## files-server

```bash
FS=~/.claude/bin/files-server
if [ -x "$FS" ]; then
  if [ "$OS" = Darwin ]; then
    launchctl list | grep -q com.user.files-server && echo "OK files-server job loaded" \
      || echo "FAIL files-server job not loaded — launchctl load -w ~/Library/LaunchAgents/com.user.files-server.plist"
    RESTART="launchctl kickstart -k gui/$(id -u)/com.user.files-server"
  else
    systemctl --user is-active --quiet files-server && echo "OK files-server service active" \
      || echo "FAIL files-server service not active — systemctl --user enable --now files-server"
    RESTART="systemctl --user restart files-server"
  fi
  PROBE=/tmp/ai-tools-doctor-probe.txt; echo ok > "$PROBE"
  URL=$("$FS" url "$PROBE")
  CODE=$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$URL")
  [ "$CODE" = 200 ] && echo "OK file server answers at $URL" \
    || echo "FAIL file server not answering at $URL (got $CODE) — $RESTART · log: /tmp/files-server.err"
else echo "FAIL ~/.claude/bin/files-server missing — rerun the installer and pick files-server"; fi
```
If Tailscale came up after the file server started, the server is stuck on this machine only:
restart it with the command in the FAIL line.

## syncthing

```bash
if pgrep -ix syncthing >/dev/null; then echo "OK Syncthing running"
elif [ "$OS" = Darwin ]; then echo "FAIL Syncthing not running — open the Syncthing app (or: brew services start syncthing)"
else echo "FAIL Syncthing not running — systemctl --user enable --now syncthing"; fi
```

## doctor

You're running it. Nothing to check.

## spec-logic-design

```bash
for s in spec logic design; do
  [ -f ~/.claude/skills/$s/SKILL.md ] && echo "OK /$s" || echo "FAIL /$s missing — rerun the installer and pick spec-logic-design"
done
[ -d ~/memory/specs ] && echo "OK ~/memory/specs" || echo "WARN ~/memory/specs not there yet — normal until the first /spec, which creates it"
```

## review-multi

```bash
if command -v codex >/dev/null; then echo "OK $(codex --version 2>/dev/null | head -1)"
  codex login status >/dev/null 2>&1 && echo "OK codex signed in" || echo "FAIL codex not signed in — run: codex login"
else echo "FAIL codex CLI missing — /review and /multi need it (Mac: brew install codex · Mac or Linux: npm install -g @openai/codex), then codex login"; fi
command -v gemini >/dev/null && echo "OK gemini CLI (optional third voice for /multi)" || echo "WARN gemini CLI not installed — optional; /multi works with Claude + codex"
```

## image

```bash
[ -f ~/.claude/skills/image/SKILL.md ] && echo "OK /image" || echo "FAIL /image missing — rerun the installer and pick image"
if [ -n "${GEMINI_API_KEY:-}" ] || [ -n "${OPENAI_API_KEY:-}" ]; then echo "OK an image API key is set"
else echo "FAIL no GEMINI_API_KEY or OPENAI_API_KEY — add one to your shell profile (e.g. export GEMINI_API_KEY=...), then restart Claude"; fi
command -v python3 >/dev/null && echo "OK python3" || echo "FAIL python3 missing — the image scripts need it (Mac: brew install python · Linux: install python3)"
```

## prototype

```bash
[ -f ~/.claude/skills/prototype/SKILL.md ] && echo "OK /prototype" || echo "FAIL /prototype missing — rerun the installer and pick prototype"
```

## Summary

Print one table — a row per section you ran — then one line with the count:

```
Result  Check
OK      Installed pieces (9) — all files present
OK      Memory folder (~/memory → ~/Sync/memory)
FAIL    rm guard not executable
OK      Transcripts
OK      Memory search, index updated 12m ago
WARN    No upkeep runs logged yet
OK      Tailscale + file server

1 FAIL, 1 WARN.
```

## After the checks

- **Fix what is safe to fix** without asking: `mkdir` a missing folder, `chmod +x` a hook,
  `qmd update && qmd embed`, restart the file server, re-load an upkeep job. Then re-run that section.
- **Ask first** before editing `~/.claude/settings.json` or `~/.claude/CLAUDE.md`, and merge — never
  overwrite.
- **Tell the user exactly what to do** for anything needing `sudo`, a password, or a click (signing
  in to Tailscale or codex, a macOS permission prompt). Wait, then re-run the section.
- A setting or MCP change only takes effect after Claude restarts — say so.
- Logs: `/tmp/qmd-upkeep.log`, `/tmp/files-server.log`, `/tmp/files-server.err`.
