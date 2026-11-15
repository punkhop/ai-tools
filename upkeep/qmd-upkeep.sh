#!/bin/bash
# qmd-upkeep — keeps memory search fresh, forever, with nobody touching it.
#
#   qmd-upkeep index    every 30 min: pick up new/changed notes, embed them (search by meaning)
#   qmd-upkeep upgrade  weekly: install the newest QMD, then re-index and tidy
#
# Why upgrade = reinstall: QMD ships a native module built against your Node
# version. Reinstalling (even the same version) rebuilds it, so a Node upgrade can
# never leave search silently broken for more than a week.
#
# Every run ends with one line: "ok" or "FAILED …" — /checkup reads the last one.
# Logs: /tmp/qmd-upkeep.log  ·  Installed to ~/.claude/bin/qmd-upkeep

set -uo pipefail
MODE="${1:-index}"
# Schedulers (launchd/systemd) start with a bare PATH — add where Node lives: the qmd and node the
# installer saved (python3 aitools.py config qmd_bin / node_bin), then the newest nvm Node, then the
# usual places. Without this, anyone whose Node comes from nvm fails every run.
CFG="$HOME/.claude/ai-tools/config.json"
saved() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],""))' "$CFG" "$1" 2>/dev/null; }
NVM=$(ls -d "$HOME"/.nvm/versions/node/*/bin 2>/dev/null | sort -V | tail -1)
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
[ -n "$NVM" ] && PATH="$NVM:$PATH"
for b in "$(saved node_bin)" "$(saved qmd_bin)"; do [ -x "$b" ] && PATH="$(dirname "$b"):$PATH"; done
LOG=/tmp/qmd-upkeep.log
exec >>"$LOG" 2>&1
echo "== $(date '+%F %T') $MODE"

QMD=$(command -v qmd) || { echo "FAILED qmd not found (PATH: $PATH) — run: python3 ~/.claude/ai-tools/src/tools/aitools.py config qmd_bin \"\$(command -v qmd)\""; exit 1; }

# After embed nothing should be waiting; notes left over mean search by meaning has stalled.
embedded() {
  local p; p=$("$QMD" status 2>/dev/null | sed -n 's/.*Pending: *\([0-9]*\).*/\1/p' | head -1)
  [ "${p:-0}" -eq 0 ] || { echo "FAILED embed left $p notes without search by meaning — run qmd embed by hand to see why"; exit 1; }
}

case "$MODE" in
  index)
    "$QMD" update && "$QMD" embed && embedded
    ;;
  upgrade)
    before=$("$QMD" --version 2>/dev/null | awk '{print $2}')
    npm install -g @tobilu/qmd@latest >/dev/null || { echo "FAILED upgrade; keeping $before"; exit 1; }
    QMD=$(command -v qmd)
    echo "qmd $before → $("$QMD" --version | awk '{print $2}')"
    "$QMD" update && "$QMD" embed && embedded && "$QMD" cleanup
    ;;
  *) echo "usage: qmd-upkeep index|upgrade" >&2; exit 2 ;;
esac
rc=$?
[ "$rc" -eq 0 ] && echo "ok" || echo "FAILED $MODE (exit $rc)"
exit "$rc"
