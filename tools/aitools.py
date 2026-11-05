#!/usr/bin/env python3
"""aitools.py — the mechanical half of the ai-tools installer. Python 3.8+, standard library only.

Claude runs it while following START-HERE.md; nobody needs to run it by hand.

  plan <ids...>                 every file: new / same / different from what is already there
  install <id> [--take|--keep]  copy one piece in, back up anything replaced, record it
  claude-md <ids...>            write the marked ai-tools block in ~/.claude/CLAUDE.md
  settings <ids...>             merge the pieces' hooks and permissions into ~/.claude/settings.json
  status                        installed pieces and versions against this copy of the repo
  uninstall [ids...]            remove what ai-tools installed (all of it when no ids)

Keys are saved by the image skill's own script: ~/.claude/skills/image/scripts/save_key.py.
Backups go to ~/.claude/ai-tools-backup/<YYYY-MM-DD>/, keeping each file's path from the home folder.
The memory folder is never touched.
"""

import datetime
import filecmp
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()
CLAUDE = HOME / ".claude"
STATE = CLAUDE / "ai-tools" / "installed.json"
CLAUDE_MD = CLAUDE / "CLAUDE.md"
SETTINGS = CLAUDE / "settings.json"
START, END = "<!-- ai-tools:start v{} -->", "<!-- ai-tools:end -->"
BLOCK = re.compile(r"\n*<!-- ai-tools:start v[^>]*-->.*?<!-- ai-tools:end -->\n?", re.S)
PLACEHOLDER = "/Users/REPLACE_WITH_YOUR_USERNAME"   # launchd files need a real home path
OS = {"Darwin": "mac", "Linux": "linux"}.get(platform.system(), "other")

MANIFEST = json.loads((REPO / "pieces.json").read_text())
PIECES = MANIFEST["pieces"]
GROUPS = json.loads((REPO / "settings" / "hooks.json").read_text())


# ---------- small helpers ----------

def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"version": MANIFEST["version"], "installed_at": None, "pieces": {}, "settings": {}}


def save_state(state):
    state["version"] = MANIFEST["version"]
    state["installed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def dest_path(to):
    return HOME / to[2:] if to.startswith("~/") else CLAUDE / to


def shown(path):
    """How a path is recorded and printed: relative to ~/.claude when inside it, else ~/..."""
    try:
        return str(path.relative_to(CLAUDE))
    except ValueError:
        return "~/" + str(path.relative_to(HOME))


def from_record(rec):
    rec = os.path.expanduser(rec)
    return Path(rec) if os.path.isabs(rec) else CLAUDE / rec


def backup(path):
    """Copy a file into today's backup folder, keeping its path from the home folder."""
    day = datetime.date.today().isoformat()
    target = HOME / ".claude" / "ai-tools-backup" / day / path.relative_to(HOME)
    if target.exists() and not filecmp.cmp(path, target, shallow=False):
        target = target.with_name(target.name + datetime.datetime.now().strftime(".%H%M%S"))
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(path, target)
    return target


def check_ids(ids):
    bad = [i for i in ids if i not in PIECES]
    if bad:
        die(f"Unknown piece: {', '.join(bad)}. Known: {', '.join(PIECES)}")


def units(piece_id):
    """Each manifest file entry as one unit: [(src, dest, exec), ...] for files on this OS.
    A folder entry is one unit, so keep/take decides a whole skill at once."""
    out = []
    for entry in PIECES[piece_id]["files"]:
        if entry.get("os") and entry["os"] != OS:
            continue
        src = REPO / entry["from"]
        if not src.exists():
            die(f"The repo is missing {entry['from']} (needed by {piece_id}).")
        if src.is_dir():
            files = sorted(p for p in src.rglob("*") if p.is_file()
                           and "__pycache__" not in p.parts and p.name != ".DS_Store")
            out.append([(f, dest_path(entry["to"]) / f.relative_to(src), entry.get("exec", False)) for f in files])
        else:
            out.append([(src, dest_path(entry["to"]), entry.get("exec", False))])
    return out


def content(src):
    data = src.read_bytes()
    if PLACEHOLDER.encode() in data:
        data = data.replace(PLACEHOLDER.encode(), str(HOME).encode())
    return data


def compare(src, dest):
    if not dest.exists():
        return "new"
    return "same" if dest.read_bytes() == content(src) else "different"


def owners(state):
    """dest path -> the installed pieces that list it."""
    out = {}
    for pid, piece in state["pieces"].items():
        for rec in piece.get("files", []):
            out.setdefault(str(from_record(rec)), []).append(pid)
    return out


# ---------- commands ----------

def cmd_plan(ids):
    check_ids(ids)
    state = load_state()
    mine = owners(state)
    chosen = set(ids) | set(state["pieces"])
    for pid in ids:
        piece = PIECES[pid]
        missing = [n for n in piece["needs"] if n not in chosen]
        notes = []
        if missing:
            notes.append("needs " + ", ".join(missing))
        if piece["t3_only"]:
            notes.append("T3 Code only")
        print(f"{pid}  ({piece['name']}){'  — ' + '; '.join(notes) if notes else ''}")
        rows = [(compare(s, d), s, d) for unit in units(pid) for s, d, _ in unit]
        if not rows:
            print("  no files (set up by hand in its stage)")
        for status, src, dest in rows:
            who = mine.get(str(dest))
            tag = f"  (installed earlier by ai-tools: {', '.join(who)})" if who and status == "different" else ""
            print(f"  {status:<9} {shown(dest)}{tag}")
            if status == "different":
                print(f"            compare: diff {dest} {src}")


def cmd_install(pid, take, keep):
    check_ids([pid])
    state = load_state()
    recorded, kept, backed = [], [], []
    for unit in units(pid):
        statuses = [compare(s, d) for s, d, _ in unit]
        if "different" in statuses and not (take or keep):
            die(f"{pid}: {shown(unit[0][1])} differs from what is already there. "
                f"Run plan, explain the difference, then install again with --take (use mine) or --keep (keep theirs).", 3)
        if "different" in statuses and keep:
            kept.append(shown(unit[0][1]))
            continue
        for (src, dest, exe), status in zip(unit, statuses):
            if status == "different":
                backed.append(shown(backup(dest)))
            if status != "same":
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(content(src))
                shutil.copymode(src, dest)
            if exe:
                dest.chmod(0o755)
            recorded.append(shown(dest))
    state["pieces"][pid] = {"version": PIECES[pid]["version"], "files": recorded}
    if kept:
        state["pieces"][pid]["kept_theirs"] = kept
    save_state(state)
    print(f"{pid}: {len(recorded)} file(s) in place" + (f", kept theirs: {', '.join(kept)}" if kept else ""))
    for b in backed:
        print(f"  backed up the old copy to ~/.claude/{b}" if not b.startswith("~/") else f"  backed up to {b}")


def block_for(ids):
    seen, lines = set(), []
    for pid in PIECES:                      # manifest order, so the block reads the same everywhere
        snippet = PIECES[pid].get("claude_md")
        for other, swap in PIECES[pid].get("claude_md_if_also", {}).items():
            if other in ids:
                snippet = swap
        if pid not in ids or not snippet:
            continue
        for line in (REPO / snippet).read_text().rstrip("\n").split("\n"):
            key = line.strip()
            if key.startswith(("@", "## ")):
                if key in seen:
                    continue
                seen.add(key)
            lines.append(line)
        lines.append("")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip("\n")
    rows = text.split("\n")                 # one list when two pieces add bullets in a row
    text = "\n".join(r for i, r in enumerate(rows) if not (
        r == "" and 0 < i < len(rows) - 1 and rows[i - 1].startswith(("- ", "  ")) and rows[i + 1].startswith("- ")))
    head = START.format(MANIFEST["version"])
    note = "<!-- Added by ai-tools. This block is replaced on update; write your own rules outside it. -->"
    return f"{head}\n{note}\n\n{text}\n\n{END}\n"


def write_claude_md(ids):
    old = CLAUDE_MD.read_text() if CLAUDE_MD.exists() else ""
    rest = BLOCK.sub("\n", old).rstrip("\n")
    new = (rest + "\n\n" if rest else "") + block_for(ids) if ids else (rest + "\n" if rest else "")
    if new == old:
        return "unchanged"
    if CLAUDE_MD.exists():
        backup(CLAUDE_MD)
    if not new:                             # the file held only the ai-tools block
        CLAUDE_MD.unlink()
        return "removed (it held only the ai-tools block)"
    CLAUDE.mkdir(parents=True, exist_ok=True)
    CLAUDE_MD.write_text(new)
    return "updated" if ids else "block removed"


def cmd_claude_md(ids):
    check_ids(ids)
    ids = set(ids) | set(load_state()["pieces"])
    print(f"~/.claude/CLAUDE.md: {write_claude_md(ids)} ({len(ids)} piece(s) in the ai-tools block)")


def read_settings():
    if not SETTINGS.exists():
        return {}
    try:
        return json.loads(SETTINGS.read_text())
    except json.JSONDecodeError as e:
        die(f"~/.claude/settings.json is not valid JSON ({e}). Nothing was changed. Fix that file first.")


def write_settings(data):
    if SETTINGS.exists():
        backup(SETTINGS)
    CLAUDE.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(json.dumps(data, indent=2) + "\n")


def merge_group(cur, group):
    """Add a group's permissions and hooks to cur. Returns only what was actually added."""
    added = {}
    for kind, items in group.get("permissions", {}).items():
        have = cur.setdefault("permissions", {}).setdefault(kind, [])
        new = [x for x in items if x not in have]
        have.extend(new)
        if new:
            added.setdefault("permissions", {})[kind] = new
    for event, entries in group.get("hooks", {}).items():
        have = cur.setdefault("hooks", {}).setdefault(event, [])
        for entry in entries:
            cmds = [h["command"] for h in entry["hooks"]]
            if all(c in json.dumps(have) for c in cmds):
                continue
            have.append(entry)
            added.setdefault("hooks", {}).setdefault(event, []).append(entry)
    return added


def cmd_settings(ids):
    check_ids(ids)
    state = load_state()
    cur = read_settings()
    before = json.dumps(cur, sort_keys=True)
    names = ["base"] + [PIECES[i]["settings"] for i in ids if PIECES[i]["settings"]]
    for name in names:
        added = merge_group(cur, GROUPS[name])
        if added:
            prev = state.setdefault("settings", {}).setdefault(name, {})
            for kind, items in added.get("permissions", {}).items():
                prev.setdefault("permissions", {}).setdefault(kind, []).extend(items)
            for event, entries in added.get("hooks", {}).items():
                prev.setdefault("hooks", {}).setdefault(event, []).extend(entries)
    if json.dumps(cur, sort_keys=True) != before:
        write_settings(cur)
        save_state(state)
        print(f"~/.claude/settings.json: merged {', '.join(names)}")
    else:
        print("~/.claude/settings.json: already had everything")


def cmd_status():
    state = load_state()
    print(f"This copy of ai-tools: {MANIFEST['version']}")
    if not state["pieces"]:
        print("Nothing installed with ai-tools yet.")
    else:
        print(f"Installed: {state.get('version')} on {state.get('installed_at')}")
    for pid, piece in PIECES.items():
        have = state["pieces"].get(pid)
        if not have:
            continue
        rows = [compare(s, d) for unit in units(pid) for s, d, _ in unit]
        changed = sum(r != "same" for r in rows)
        if have["version"] != piece["version"]:
            word = f"update {have['version']} → {piece['version']}"
        elif changed:
            word = f"{changed} file(s) differ from this copy"
        else:
            word = "up to date"
        print(f"  {pid:<18} {word}")
    new = [p for p in PIECES if p not in state["pieces"]]
    if state["pieces"] and new:
        print("Not installed: " + ", ".join(new))


def remove_settings(state, groups_to_remove, keep_groups):
    cur = read_settings()
    before = json.dumps(cur, sort_keys=True)
    still = json.dumps([GROUPS[g] for g in keep_groups])
    for name in groups_to_remove:
        added = state.get("settings", {}).pop(name, {})
        for kind, items in added.get("permissions", {}).items():
            have = cur.get("permissions", {}).get(kind, [])
            for x in items:
                if x in have and json.dumps(x) not in still:
                    have.remove(x)
        for event, entries in added.get("hooks", {}).items():
            have = cur.get("hooks", {}).get(event, [])
            for entry in entries:
                if entry in have:
                    have.remove(entry)
            if event in cur.get("hooks", {}) and not have:
                del cur["hooks"][event]
    for key in ("permissions", "hooks"):
        sub = cur.get(key)
        if isinstance(sub, dict):
            for k in [k for k, v in sub.items() if v == []]:
                del sub[k]
            if not sub:
                del cur[key]
    if json.dumps(cur, sort_keys=True) == before:
        return
    if cur:
        write_settings(cur)
    else:                                   # it held only what ai-tools added
        backup(SETTINGS)
        SETTINGS.unlink()


def prune_empty(path):
    stop = {CLAUDE, HOME, HOME / ".config", HOME / ".config" / "systemd" / "user",
            HOME / "Library", HOME / "Library" / "LaunchAgents"}
    path = path.parent
    while path not in stop and HOME in path.parents and path.is_dir() and not any(path.iterdir()):
        path.rmdir()
        path = path.parent


def cmd_uninstall(ids):
    check_ids(ids)
    state = load_state()
    everything = not ids
    ids = list(state["pieces"]) if everything else [i for i in ids if i in state["pieces"]]
    if not ids and not state.get("settings"):
        print("Nothing to uninstall.")
        return
    remaining = [p for p in state["pieces"] if p not in ids]
    still_used = {str(from_record(r)) for p in remaining for r in state["pieces"][p].get("files", [])}
    removed = 0
    for pid in ids:
        for rec in state["pieces"][pid].get("files", []):
            path = from_record(rec)
            if str(path) in still_used or not path.exists():
                continue
            path.unlink()
            prune_empty(path)
            removed += 1
        del state["pieces"][pid]
    groups = [PIECES[p]["settings"] for p in ids if PIECES[p]["settings"]] + (["base"] if everything else [])
    keep = ["base"] * (not everything) + [PIECES[p]["settings"] for p in remaining if PIECES[p]["settings"]]
    remove_settings(state, groups, keep)
    print(f"Removed {removed} file(s) from {len(ids)} piece(s).")
    print(f"~/.claude/CLAUDE.md: {write_claude_md(set(remaining))}")
    if remaining or state.get("settings"):
        save_state(state)
    elif STATE.exists():
        STATE.unlink()
        print("Left in place: ~/memory, ~/.claude/ai-tools-backup, and ~/.claude/ai-tools "
              "(this copy of the repo and any saved keys).")


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    flags = {a for a in args if a.startswith("--")}
    ids = [a for a in args if not a.startswith("--")]
    if cmd == "plan" and ids:
        cmd_plan(ids)
    elif cmd == "install" and len(ids) == 1 and not flags - {"--take", "--keep"} and len(flags) < 2:
        cmd_install(ids[0], "--take" in flags, "--keep" in flags)
    elif cmd == "claude-md":
        cmd_claude_md(ids)
    elif cmd == "settings":
        cmd_settings(ids)
    elif cmd == "status":
        cmd_status()
    elif cmd == "uninstall":
        cmd_uninstall(ids)
    else:
        die(__doc__, 2)


if __name__ == "__main__":
    main(sys.argv[1:])
