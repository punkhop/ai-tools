#!/bin/bash
# files-server — one always-on static http server so every page, note and screenshot
# Claude makes is a CLICKABLE http link: in the terminal, in T3 Code, on your laptop,
# on your phone.
#
# Why http and not file://: terminals and Claude Code only turn http(s):// into
# clickable links, never file://, and file:// is useless from another device.
#
# The hostname in every link is this machine's Tailscale name (MagicDNS), so ONE link
# shape — http://<machine>:8181/... — works from every device on your tailnet,
# at home or away.
#
# Security: serves a CURATED set of folders (memory, dev, /tmp, the html assets) —
# never $HOME wholesale, so ~/.ssh and secrets are unreachable. Read-only.
# It binds to the Tailscale address ONLY, so nobody on your home or cafe Wi-Fi can
# read it. If Tailscale is down it binds 127.0.0.1 (fails closed: links break loudly
# instead of exposing your files to the LAN).
#
# Path -> URL:
#   ~/memory/X                      -> http://<host>:PORT/memory/X
#   ~/dev/X                         -> http://<host>:PORT/dev/X
#   /tmp/X                          -> http://<host>:PORT/tmp/X
#   ~/.claude/skills/html/assets/X  -> http://<host>:PORT/assets/X
#
# Usage:
#   files-server                 start (default) — what the LaunchAgent / systemd unit runs
#   files-server url <abs-path>  print the http URL for a file
#   files-server stop
#
# Env overrides: FILES_SERVER_PORT, FILES_SERVER_HOST, FILES_SERVER_BIND,
#                MEMORY_ROOT, DEV_ROOT

set -u
PORT="${FILES_SERVER_PORT:-8181}"
MEMORY_ROOT="${MEMORY_ROOT:-$HOME/memory}"
DEV_ROOT="${DEV_ROOT:-$HOME/dev}"
ASSETS="$HOME/.claude/skills/html/assets"
ROOT="$HOME/.local/share/files-server"
SELF_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")" && pwd)"

# Link host: this machine's Tailscale name if Tailscale knows it, else the short hostname.
ts_name() {
  local ts; ts="$(command -v tailscale || echo /Applications/Tailscale.app/Contents/MacOS/Tailscale)"
  [ -x "$ts" ] || return 0
  "$ts" status --json 2>/dev/null | python3 -c \
    'import sys,json; print(json.load(sys.stdin)["Self"]["DNSName"].split(".")[0])' 2>/dev/null
}
HOST="${FILES_SERVER_HOST:-$(ts_name)}"
HOST="${HOST:-$(hostname -s)}"
HOST="$(printf '%s' "$HOST" | tr 'A-Z' 'a-z')"

# This machine's tailnet address (100.64.0.0/10). Absolute ifconfig path: launchd's PATH
# has no /sbin. Linux has no ifconfig; `ip` prints the same "inet <addr>" shape.
tailnet_ip() {
  { /sbin/ifconfig 2>/dev/null || ip -4 -o addr 2>/dev/null; } \
    | grep -oE 'inet 100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])\.[0-9]{1,3}\.[0-9]{1,3}' \
    | awk '{print $2}' | head -1
}

build_root() {
  mkdir -p "$ROOT"
  ln -sfn "$MEMORY_ROOT" "$ROOT/memory"
  ln -sfn "/tmp"         "$ROOT/tmp"
  # Linked even if missing yet: the link starts working the moment the folder appears
  # (the /html skill is installed after the server starts), no restart needed.
  ln -sfn "$DEV_ROOT" "$ROOT/dev"
  ln -sfn "$ASSETS"   "$ROOT/assets"
}

url_for() {
  local p
  p="$(cd "$(dirname "$1")" 2>/dev/null && pwd -P)/$(basename "$1")" || p="$1"
  local mem dev assets
  # A folder that doesn't exist yet gets a placeholder that never matches; an empty value
  # would turn "$dev/"* into "/"* and claim every path on the disk.
  mem="$(cd "$MEMORY_ROOT" 2>/dev/null && pwd -P)"; mem="${mem:-/nonexistent-memory}"
  dev="$(cd "$DEV_ROOT" 2>/dev/null && pwd -P)"; dev="${dev:-/nonexistent-dev}"
  assets="$(cd "$ASSETS" 2>/dev/null && pwd -P)"; assets="${assets:-/nonexistent-assets}"
  case "$p" in
    "$mem/"*)    printf 'http://%s:%s/memory/%s\n' "$HOST" "$PORT" "${p#"$mem"/}" ;;
    "$dev/"*)    printf 'http://%s:%s/dev/%s\n'    "$HOST" "$PORT" "${p#"$dev"/}" ;;
    /tmp/*|/private/tmp/*) printf 'http://%s:%s/tmp/%s\n' "$HOST" "$PORT" "${p#*/tmp/}" ;;
    "$assets/"*) printf 'http://%s:%s/assets/%s\n' "$HOST" "$PORT" "${p#"$assets"/}" ;;
    *) echo "not under a served folder (memory, dev, /tmp): $p" >&2; return 1 ;;
  esac
}

case "${1:-start}" in
  -h|--help) sed -n '2,33p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  url) shift; url_for "$1"; exit $? ;;
  stop) pkill -f "files-server-serve.py $PORT" && echo "stopped" || echo "not running"; exit 0 ;;
  start)
    build_root
    BIND="${FILES_SERVER_BIND:-$(tailnet_ip)}"
    # At boot the server can start before Tailscale is up. Wait for it rather than
    # settling on loopback forever.
    if [ -z "$BIND" ]; then
      for _ in $(seq 1 30); do sleep 2; BIND="$(tailnet_ip)"; [ -n "$BIND" ] && break; done
    fi
    BIND="${BIND:-127.0.0.1}"
    cd "$ROOT" || exit 1
    echo "files-server on $BIND:$PORT → http://$HOST:$PORT/"
    # On a Mac use Apple's python: the firewall trusts a binary by path, and Homebrew's
    # python changes path on every upgrade, which silently blocks all connections.
    PYTHON=python3
    [ "$(uname -s)" = "Darwin" ] && [ -x /usr/bin/python3 ] && PYTHON=/usr/bin/python3
    exec "$PYTHON" "$SELF_DIR/files-server-serve.py" "$PORT" "$ROOT" "$BIND"
    ;;
  *) echo "unknown arg: $1 (try --help)" >&2; exit 2 ;;
esac
