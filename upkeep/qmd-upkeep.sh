#!/bin/bash
# qmd-upkeep — keeps memory search fresh, forever, with nobody touching it.
#
#   qmd-upkeep index    every 30 min: pick up new/changed notes, embed them
#   qmd-upkeep upgrade  weekly: install the newest QMD, then re-index and tidy
#
# Why upgrade = reinstall: QMD ships a native module built against your Node
# version. Reinstalling (even the same version) rebuilds it, so a Node upgrade can
# never leave search silently broken for more than a week.
#
# Every run ends with one line: "ok" or "FAILED …" — /doctor reads the last one.
# Logs: /tmp/qmd-upkeep.log  ·  Installed to ~/.claude/bin/qmd-upkeep

set -uo pipefail
MODE="${1:-index}"
# Schedulers (launchd/systemd) start with a bare PATH — add where Node lives.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
LOG=/tmp/qmd-upkeep.log
exec >>"$LOG" 2>&1
echo "== $(date '+%F %T') $MODE"

QMD=$(command -v qmd) || { echo "FAILED qmd not installed — run the kit's QMD stage"; exit 1; }

case "$MODE" in
  index)
    "$QMD" update && "$QMD" embed
    ;;
  upgrade)
    before=$("$QMD" --version 2>/dev/null | awk '{print $2}')
    npm install -g @tobilu/qmd@latest >/dev/null || { echo "FAILED upgrade; keeping $before"; exit 1; }
    QMD=$(command -v qmd)
    echo "qmd $before → $("$QMD" --version | awk '{print $2}')"
    "$QMD" update && "$QMD" embed && "$QMD" cleanup
    ;;
  *) echo "usage: qmd-upkeep index|upgrade" >&2; exit 2 ;;
esac
rc=$?
[ "$rc" -eq 0 ] && echo "ok" || echo "FAILED $MODE (exit $rc)"
exit "$rc"
