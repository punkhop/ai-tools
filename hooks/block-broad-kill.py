#!/usr/bin/env python3
"""
PreToolUse hook (Bash): block process kills that would take out programs you are using.

Why: `pkill -f "cat"` meant to stop one stray `cat` also matches "Applications", so it quits
every open app, the terminal among them. Claude reaches for broad kills like that when it cleans
up a dev server.

How it judges: it doesn't guess from the pattern. It dry-runs the same match with
read-only `pgrep` and looks at who WOULD die:
  - Chrome / Chromium / headless-shell processes  -> always fine (broken browsers)
  - any other app (a Mac .app, a Linux program started from /usr or /opt), a Claude session,
    a system daemon -> block
  - more than MAX_VICTIMS ordinary processes      -> block (pattern too broad)
  - `kill -1` / `kill -- -1` (every process you own) -> block
Everything else (a dev server, a stuck vitest, a named pid) passes.

Exit 0 = allow | 2 = block with feedback.
Escape hatch: literal ALLOW_BROAD_KILL=1 in the command (only when the user says so).
"""
import json
import re
import shlex
import subprocess
import sys

MAX_VICTIMS = 10
CHROME = re.compile(r"Google Chrome|Chromium|chrome-headless-shell|chromedriver|/chrome(\s|$)", re.I)
PROTECTED = re.compile(
    r"\.app/|(^|/)claude(\s|$)|/\.local/share/claude|WindowServer|loginwindow|/System/Library/|/usr/libexec/|/usr/sbin/"
    r"|^/usr/(bin|lib|lib64|share)/|^/opt/",   # Linux: desktop and system programs started by full path
)
SIGNAL_TOKEN = re.compile(r"^-(\d+|[A-Z]+|SIG[A-Z]+)$")
SEPARATORS = {"&&", "||", "|", ";", "&"}

def segments(tokens):
    seg = []
    for t in tokens:
        if t in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)
    if seg:
        yield seg

def clean(tok):
    # Unexpanded shell vars ($$, $PID) become a pid that can't exist — matches nothing.
    return "99999999" if "$" in tok else tok

def pgrep_args(seg):
    """Turn a pkill/killall/pgrep segment into read-only pgrep args, or None."""
    base = seg[0].rsplit("/", 1)[-1]
    rest = [clean(t) for t in seg[1:] if not re.match(r"^\d*[<>]", t)]
    if base in ("pkill", "pgrep"):
        return ["-l", "-a"] + [t for t in rest if not SIGNAL_TOKEN.match(t) and t != "-l"]
    if base == "killall":
        regex = "-m" in rest
        names, skip = [], False
        for t in rest:
            if skip:
                skip = False
                continue
            if t in ("-u", "-t", "-c", "-SIGNAL"):
                skip = True
                continue
            if t.startswith("-"):
                continue
            names.append(t)
        if not names:
            return None
        pat = "|".join(names if regex else ["^(%s)$" % re.escape(n) for n in names])
        return ["-l", "-a", pat]
    return None

def victims(args):
    try:
        out = subprocess.run(["/usr/bin/pgrep"] + args, capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return []
    procs = []
    for line in out.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if pid.isdigit():
            procs.append((int(pid), cmd))
    # pgrep -l without -f prints only the name; fetch full paths for judging.
    if procs:
        try:
            ps = subprocess.run(["/bin/ps", "-o", "pid=,args=", "-p", ",".join(str(p) for p, _ in procs)],
                                capture_output=True, text=True, timeout=5).stdout
            full = {}
            for line in ps.splitlines():
                pid, _, cmd = line.strip().partition(" ")
                if pid.isdigit():
                    full[int(pid)] = cmd.strip()
            procs = [(p, full.get(p, c)) for p, c in procs]
        except Exception:
            pass
    return procs

def block(reason, sample):
    lines = "\n".join("  " + c[:140] for c in sample[:8])
    sys.stderr.write(f"""BLOCKED: this kill is too broad — {reason}.

It would hit (dry run via pgrep):
{lines}

A pattern like `pkill -f "cat"` also matches "Applications" and quits every open app.
Kill by PID instead: find it (`lsof -nP -iTCP:PORT -sTCP:LISTEN`, or `pgrep -lf '<full path>'`),
check it with `ps -p <pid> -o args`, then `kill <pid>`.
Chrome/Chromium processes are always allowed. Escape hatch (only on the user's word): ALLOW_BROAD_KILL=1
""")
    sys.exit(2)

def main():
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except Exception:
        sys.exit(0)
    if not cmd or not re.search(r"\b(pkill|killall|kill)\b", cmd):
        sys.exit(0)
    if "ALLOW_BROAD_KILL=1" in cmd:
        sys.exit(0)
    try:
        tokens = shlex.split(cmd.replace("\n", " ; "), posix=True)
    except ValueError:
        sys.exit(0)

    kills = "kill" in {t.rsplit("/", 1)[-1] for t in tokens} or "xargs" in tokens
    for seg in segments(tokens):
        base = seg[0].rsplit("/", 1)[-1]
        if base == "kill" and seg[-1] == "-1":
            block("`kill -1` signals every process you own", ["(every process you own)"])
        if base == "pgrep" and not kills:
            continue  # a plain lookup, nothing dies
        args = pgrep_args(seg)
        if args is None:
            continue
        procs = [(p, c) for p, c in victims(args) if not CHROME.search(c)]
        protected = [c for _, c in procs if PROTECTED.search(c)]
        if protected:
            block("it matches apps or system processes", protected)
        if len(procs) > MAX_VICTIMS:
            block(f"it matches {len(procs)} processes", [c for _, c in procs])
    sys.exit(0)

if __name__ == "__main__":
    main()
